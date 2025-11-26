/// <reference types="vitest" />
import { describe, expect, it } from 'vitest'
import {
  coordsEqual,
  inBounds,
  randomEmptyCell,
  toCoord,
  toIndex,
  type BoardConfig,
} from './board'

const smallBoard: BoardConfig = { rows: 4, cols: 4, cellSize: 10 }

describe('board utils', () => {
  it('checks bounds correctly', () => {
    expect(inBounds({ row: 0, col: 0 }, smallBoard)).toBe(true)
    expect(inBounds({ row: 3, col: 3 }, smallBoard)).toBe(true)
    expect(inBounds({ row: -1, col: 0 }, smallBoard)).toBe(false)
    expect(inBounds({ row: 4, col: 0 }, smallBoard)).toBe(false)
  })

  it('matches coordinates and converts indices', () => {
    expect(coordsEqual({ row: 1, col: 1 }, { row: 1, col: 1 })).toBe(true)
    expect(coordsEqual({ row: 1, col: 1 }, { row: 1, col: 2 })).toBe(false)

    const index = toIndex({ row: 2, col: 3 }, smallBoard)
    expect(index).toBe(11)
    expect(toCoord(index, smallBoard)).toEqual({ row: 2, col: 3 })
  })

  it('finds empty cells outside occupied ones', () => {
    const occupied = [
      { row: 0, col: 0 },
      { row: 0, col: 1 },
      { row: 1, col: 0 },
    ]
    const empty = randomEmptyCell(occupied, smallBoard)
    expect(inBounds(empty, smallBoard)).toBe(true)
    expect(
      occupied.some((coord) => coord.row === empty.row && coord.col === empty.col),
    ).toBe(false)
  })
})
