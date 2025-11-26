import type { Direction } from '../hooks'

type Props = {
  onDirection: (dir: Direction) => void
  disabled?: boolean
}

export function DirectionPad({ onDirection, disabled = false }: Props) {
  const handle = (dir: Direction) => {
    if (disabled) return
    onDirection(dir)
  }

  return (
    <div className="direction-pad" aria-label="Directional controls">
      <div className="direction-pad__row">
        <span />
        <button type="button" onClick={() => handle('up')} aria-label="Up" disabled={disabled}>
          ↑
        </button>
        <span />
      </div>
      <div className="direction-pad__row">
        <button type="button" onClick={() => handle('left')} aria-label="Left" disabled={disabled}>
          ←
        </button>
        <span className="direction-pad__center" />
        <button type="button" onClick={() => handle('right')} aria-label="Right" disabled={disabled}>
          →
        </button>
      </div>
      <div className="direction-pad__row">
        <span />
        <button type="button" onClick={() => handle('down')} aria-label="Down" disabled={disabled}>
          ↓
        </button>
        <span />
      </div>
    </div>
  )
}
