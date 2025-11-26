import type { BoardConfig, Coord } from '../utils'
import { coordKey, coordsEqual, toCoord } from '../utils'
import type { GameStatus } from '../hooks'

type Props = {
  config: BoardConfig
  snake: Coord[]
  food: Coord
  status: GameStatus
}

const getCellClass = (
  coord: Coord,
  head: Coord,
  snakeSet: Set<string>,
  food: Coord,
): string => {
  if (coordsEqual(coord, head)) return 'cell cell--head'
  if (snakeSet.has(coordKey(coord))) return 'cell cell--snake'
  if (coordsEqual(coord, food)) return 'cell cell--food'
  return 'cell'
}

export function GameBoard({ config, snake, food, status }: Props) {
  const totalCells = config.rows * config.cols
  const head = snake[0]
  const snakeSet = new Set(snake.map(coordKey))

  return (
    <div
      className={`board board--${status}`}
      style={{
        gridTemplateColumns: `repeat(${config.cols}, ${config.cellSize}px)`,
        gridTemplateRows: `repeat(${config.rows}, ${config.cellSize}px)`,
      }}
    >
      {Array.from({ length: totalCells }, (_, index) => {
        const coord = toCoord(index, config)
        const cellClass = getCellClass(coord, head, snakeSet, food)
        return <div key={coordKey(coord)} className={cellClass} />
      })}
    </div>
  )
}
