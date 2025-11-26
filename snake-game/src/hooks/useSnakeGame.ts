import { useCallback, useEffect, useRef, useState } from 'react'
import type { BoardConfig, Coord } from '../utils'
import { DEFAULT_BOARD, coordsEqual, inBounds, randomEmptyCell } from '../utils'

export type GameStatus = 'idle' | 'playing' | 'paused' | 'gameover'
export type Direction = 'up' | 'down' | 'left' | 'right'
export type GameMode = 'walls' | 'pass-through'

type GameState = {
  snake: Coord[]
  direction: Direction
  food: Coord
  status: GameStatus
  score: number
  speed: number
  highScore: number
}

const DIRECTION_VECTORS: Record<Direction, Coord> = {
  up: { row: -1, col: 0 },
  down: { row: 1, col: 0 },
  left: { row: 0, col: -1 },
  right: { row: 0, col: 1 },
}

const isReverse = (current: Direction, next: Direction) =>
  (current === 'up' && next === 'down') ||
  (current === 'down' && next === 'up') ||
  (current === 'left' && next === 'right') ||
  (current === 'right' && next === 'left')

const createInitialState = (config: BoardConfig): GameState => {
  const midRow = Math.floor(config.rows / 2)
  const midCol = Math.floor(config.cols / 2)
  const snake: Coord[] = [
    { row: midRow, col: midCol + 1 },
    { row: midRow, col: midCol },
    { row: midRow, col: midCol - 1 },
  ]

  const food = randomEmptyCell(snake, config)

  return {
    snake,
    direction: 'right',
    food,
    status: 'idle',
    score: 0,
    speed: 220,
    highScore: 0,
  }
}

const HIGH_SCORE_KEY = 'snake.highScore'
const SOUND_ENABLED_KEY = 'snake.soundEnabled'

const readBoolean = (key: string, fallback: boolean) => {
  try {
    if (typeof window === 'undefined') return fallback
    const raw = window.localStorage.getItem(key)
    if (raw === null) return fallback
    return raw === 'true'
  } catch {
    return fallback
  }
}

const readNumber = (key: string, fallback: number) => {
  try {
    if (typeof window === 'undefined') return fallback
    const raw = window.localStorage.getItem(key)
    if (raw === null) return fallback
    const parsed = Number.parseInt(raw, 10)
    return Number.isFinite(parsed) ? parsed : fallback
  } catch {
    return fallback
  }
}

export const useSnakeGame = (config: BoardConfig = DEFAULT_BOARD) => {
  const [state, setState] = useState<GameState>(() => {
    const initialHighScore = readNumber(HIGH_SCORE_KEY, 0)
    return { ...createInitialState(config), highScore: initialHighScore }
  })
  const [soundEnabled, setSoundEnabled] = useState<boolean>(() => readBoolean(SOUND_ENABLED_KEY, true))
  const [mode, setMode] = useState<GameMode>('walls')
  const pendingDirectionRef = useRef<Direction>('right')
  const prevScoreRef = useRef<number>(state.score)
  const prevStatusRef = useRef<GameStatus>(state.status)
  const soundEnabledRef = useRef<boolean>(soundEnabled)
  const audioContextRef = useRef<AudioContext | null>(null)

  soundEnabledRef.current = soundEnabled

  const requestDirection = useCallback(
    (next: Direction) => {
      setState((prev) => {
        if (prev.status === 'idle' || prev.status === 'gameover') {
          return prev
        }

        if (isReverse(prev.direction, next) && prev.snake.length > 1) {
          return prev
        }

        pendingDirectionRef.current = next
        if (prev.snake.length <= 1) {
          return { ...prev, direction: next }
        }

        return prev
      })
    },
    [],
  )

  const tick = useCallback(() => {
    setState((prev) => {
      if (prev.status !== 'playing') return prev

      const direction = pendingDirectionRef.current ?? prev.direction
      const vector = DIRECTION_VECTORS[direction]
      const head = prev.snake[0]
      let newHead = { row: head.row + vector.row, col: head.col + vector.col }

      if (!inBounds(newHead, config)) {
        if (mode === 'walls') {
          return { ...prev, status: 'gameover' }
        }
        // Wrap around for pass-through mode
        newHead = {
          row: (newHead.row + config.rows) % config.rows,
          col: (newHead.col + config.cols) % config.cols,
        }
      }

      const hitsSelf = prev.snake.some((segment) => coordsEqual(segment, newHead))
      if (hitsSelf) {
        return { ...prev, status: 'gameover' }
      }

      const ateFood = coordsEqual(newHead, prev.food)
      const grownSnake = ateFood ? [newHead, ...prev.snake] : [newHead, ...prev.snake.slice(0, -1)]

      let nextFood = prev.food
      let nextScore = prev.score
      let nextSpeed = prev.speed
      let nextHighScore = prev.highScore

      if (ateFood) {
        nextScore += 10
        nextSpeed = Math.max(120, prev.speed - 4)
        nextFood = randomEmptyCell(grownSnake, config)
        nextHighScore = Math.max(prev.highScore, nextScore)
      }

      return {
        ...prev,
        snake: grownSnake,
        direction,
        food: nextFood,
        score: nextScore,
        speed: nextSpeed,
        highScore: nextHighScore,
      }
    })
  }, [config, mode])

  useEffect(() => {
    if (state.status !== 'playing') return
    const id = window.setInterval(tick, state.speed)
    return () => window.clearInterval(id)
  }, [state.status, state.speed, tick])

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      const keyMap: Record<string, Direction> = {
        ArrowUp: 'up',
        ArrowDown: 'down',
        ArrowLeft: 'left',
        ArrowRight: 'right',
        w: 'up',
        W: 'up',
        s: 'down',
        S: 'down',
        a: 'left',
        A: 'left',
        d: 'right',
        D: 'right',
      }

      const dir = keyMap[event.key]
      if (!dir) return
      event.preventDefault()
      requestDirection(dir)
    }

    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [requestDirection])

  const start = useCallback(() => {
    setState((prev) => {
      if (prev.status === 'playing') return prev
      const initial = createInitialState(config)
      pendingDirectionRef.current = initial.direction
      return { ...initial, status: 'playing', highScore: prev.highScore }
    })
  }, [config])

  const pause = useCallback(() => {
    setState((prev) => (prev.status === 'playing' ? { ...prev, status: 'paused' } : prev))
  }, [])

  const resume = useCallback(() => {
    setState((prev) => (prev.status === 'paused' ? { ...prev, status: 'playing' } : prev))
  }, [])

  const restart = useCallback(() => {
    setState((prev) => {
      const initial = createInitialState(config)
      pendingDirectionRef.current = initial.direction
      return { ...initial, status: 'playing', highScore: prev.highScore }
    })
  }, [config])

  const changeMode = useCallback((nextMode: GameMode) => {
    setMode(nextMode)
    setState((prev) => {
      const initial = createInitialState(config)
      pendingDirectionRef.current = initial.direction
      return { ...initial, status: 'idle', highScore: prev.highScore }
    })
  }, [config])

  const toggleSound = useCallback(() => {
    setSoundEnabled((prev) => !prev)
  }, [])

  const ensureAudioContext = () => {
    if (typeof window === 'undefined') return null
    if (!audioContextRef.current) {
      try {
        audioContextRef.current = new AudioContext()
      } catch {
        audioContextRef.current = null
      }
    }
    return audioContextRef.current
  }

  const playTone = useCallback(
    (frequency: number, durationMs = 140) => {
      if (!soundEnabledRef.current) return
      const ctx = ensureAudioContext()
      if (!ctx) return

      const oscillator = ctx.createOscillator()
      const gain = ctx.createGain()
      oscillator.frequency.value = frequency
      gain.gain.setValueAtTime(0.08, ctx.currentTime)
      gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + durationMs / 1000)
      oscillator.connect(gain)
      gain.connect(ctx.destination)
      oscillator.start()
      oscillator.stop(ctx.currentTime + durationMs / 1000)
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [],
  )

  useEffect(() => {
    if (typeof window === 'undefined') return
    try {
      window.localStorage.setItem(HIGH_SCORE_KEY, state.highScore.toString())
    } catch {
      // ignore storage errors
    }
  }, [state.highScore])

  useEffect(() => {
    if (typeof window === 'undefined') return
    try {
      window.localStorage.setItem(SOUND_ENABLED_KEY, soundEnabled.toString())
    } catch {
      // ignore storage errors
    }
  }, [soundEnabled])

  useEffect(() => {
    if (state.score > prevScoreRef.current) {
      playTone(660, 110)
    }
    prevScoreRef.current = state.score
  }, [state.score, playTone])

  useEffect(() => {
    if (prevStatusRef.current !== 'gameover' && state.status === 'gameover') {
      playTone(180, 260)
    }
    prevStatusRef.current = state.status
  }, [state.status, playTone])

  return {
    state,
    config,
    start,
    pause,
    resume,
    restart,
    requestDirection,
    soundEnabled,
    toggleSound,
    mode,
    changeMode,
  }
}
