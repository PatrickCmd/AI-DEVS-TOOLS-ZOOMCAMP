export type Coord = { row: number; col: number }

export type BoardConfig = {
  rows: number
  cols: number
  cellSize: number
}

export const DEFAULT_BOARD: BoardConfig = {
  rows: 20,
  cols: 20,
  cellSize: 22,
}

export const coordKey = (coord: Coord) => `${coord.row}-${coord.col}`

export const coordsEqual = (a: Coord, b: Coord) => a.row === b.row && a.col === b.col

export const inBounds = (coord: Coord, config: BoardConfig = DEFAULT_BOARD) =>
  coord.row >= 0 && coord.col >= 0 && coord.row < config.rows && coord.col < config.cols

export const randomCell = (config: BoardConfig = DEFAULT_BOARD): Coord => ({
  row: Math.floor(Math.random() * config.rows),
  col: Math.floor(Math.random() * config.cols),
})

export const randomEmptyCell = (
  occupied: Coord[],
  config: BoardConfig = DEFAULT_BOARD,
): Coord => {
  const occupiedSet = new Set(occupied.map(coordKey))
  const totalCells = config.rows * config.cols
  if (occupiedSet.size >= totalCells) {
    throw new Error('No empty cells available on the board')
  }

  // Try random sampling first, then fall back to a linear scan to guarantee a result.
  for (let attempts = 0; attempts < 50; attempts += 1) {
    const candidate = randomCell(config)
    if (!occupiedSet.has(coordKey(candidate))) {
      return candidate
    }
  }

  for (let row = 0; row < config.rows; row += 1) {
    for (let col = 0; col < config.cols; col += 1) {
      const candidate = { row, col }
      if (!occupiedSet.has(coordKey(candidate))) {
        return candidate
      }
    }
  }

  throw new Error('Failed to find an empty cell')
}

export const toIndex = (coord: Coord, config: BoardConfig = DEFAULT_BOARD) =>
  coord.row * config.cols + coord.col

export const toCoord = (index: number, config: BoardConfig = DEFAULT_BOARD): Coord => ({
  row: Math.floor(index / config.cols),
  col: index % config.cols,
})
