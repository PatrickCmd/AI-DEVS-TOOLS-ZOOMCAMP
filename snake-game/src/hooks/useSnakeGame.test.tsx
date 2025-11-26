/// <reference types="vitest" />
import { act, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { useSnakeGame } from './useSnakeGame'
import type { BoardConfig } from '../utils'

const testBoard: BoardConfig = {
  rows: 8,
  cols: 8,
  cellSize: 20,
}

describe('useSnakeGame', () => {
  beforeEach(() => {
    window.localStorage.clear()
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('starts the game and moves right on tick', () => {
    const { result } = renderHook(() => useSnakeGame(testBoard))
    act(() => result.current.start())
    const startHead = result.current.state.snake[0]

    act(() => {
      vi.advanceTimersByTime(result.current.state.speed + 5)
    })

    expect(result.current.state.status).toBe('playing')
    expect(result.current.state.snake[0].col).toBe(startHead.col + 1)
  })

  it('prevents 180° reversal when snake length > 1', () => {
    const { result } = renderHook(() => useSnakeGame(testBoard))
    act(() => result.current.start())
    const startHead = result.current.state.snake[0]

    act(() => result.current.requestDirection('left'))
    act(() => {
      vi.advanceTimersByTime(result.current.state.speed + 5)
    })

    expect(result.current.state.snake[0].col).toBe(startHead.col + 1)
  })

  it('pauses and resumes without moving while paused', () => {
    const { result } = renderHook(() => useSnakeGame(testBoard))
    act(() => result.current.start())
    act(() => {
      vi.advanceTimersByTime(result.current.state.speed + 5)
    })
    const positionBeforePause = result.current.state.snake[0]

    act(() => result.current.pause())
    act(() => {
      vi.advanceTimersByTime(result.current.state.speed * 2)
    })
    expect(result.current.state.snake[0]).toEqual(positionBeforePause)
    expect(result.current.state.status).toBe('paused')

    act(() => result.current.resume())
    act(() => {
      vi.advanceTimersByTime(result.current.state.speed + 5)
    })
    expect(result.current.state.status).toBe('playing')
    expect(result.current.state.snake[0]).not.toEqual(positionBeforePause)
  })

  it('reads persisted high score and preserves it on start', () => {
    window.localStorage.setItem('snake.highScore', '50')
    const { result } = renderHook(() => useSnakeGame(testBoard))
    expect(result.current.state.highScore).toBe(50)
    act(() => result.current.start())
    expect(result.current.state.highScore).toBe(50)
  })

  it('respects stored sound preference and toggles it', () => {
    window.localStorage.setItem('snake.soundEnabled', 'false')
    const { result } = renderHook(() => useSnakeGame(testBoard))
    expect(result.current.soundEnabled).toBe(false)
    act(() => result.current.toggleSound())
    expect(result.current.soundEnabled).toBe(true)
  })

  it('wraps through edges in pass-through mode instead of game over', () => {
    const { result } = renderHook(() => useSnakeGame({ rows: 4, cols: 4, cellSize: 20 }))
    act(() => result.current.changeMode('pass-through'))
    act(() => result.current.start())

    // Move enough steps to cross the right wall and wrap
    act(() => {
      vi.advanceTimersByTime(result.current.state.speed * 5)
    })

    expect(result.current.state.status).toBe('playing')
    expect(result.current.state.snake[0].col).toBeLessThan(4)
  })

  it('stops the game on wall collision in walls mode', () => {
    const { result } = renderHook(() => useSnakeGame({ rows: 3, cols: 3, cellSize: 20 }))
    act(() => result.current.changeMode('walls'))
    act(() => result.current.start())

    act(() => {
      vi.advanceTimersByTime(result.current.state.speed * 5)
    })

    expect(result.current.state.status).toBe('gameover')
  })
})
