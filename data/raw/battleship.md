# Battleship

## 1. Components and Standard Fleet
- **Objective**: Sink the entire opposing fleet before yours is destroyed.
- **Grids**: Each player needs one ocean grid for placing ships and one targeting grid for recording shots. A standard grid contains 100 squares arranged in ten columns (A-J) and ten rows (1-10). Coordinates combine a letter and number (e.g., C7).
- **Standard Fleet**:
  - **Carrier**: 5 squares (Abbreviation: C)
  - **Battleship**: 4 squares (Abbreviation: B)
  - **Cruiser**: 3 squares (Abbreviation: Cr)
  - **Submarine**: 3 squares (Abbreviation: S)
  - **Destroyer**: 2 squares (Abbreviation: D)

## 2. Game Preparation
- **Prepare the play area**: Sit opposite one another with screens or folders so neither can see the other's grid. Place all markers and tools within reach. Decide first player via coin toss or alternation.
- **Deploy the fleet**: Place each ship entirely inside your ocean grid horizontally or vertically. Diagonal ships, bent ships, or overlapping ships are illegal. Once the first legal shot is called, positions are locked. Each player must verify they have exactly 17 occupied squares ($5+4+3+3+2$).

## 3. Core Turn Sequence
Players alternate turns consisting of these steps:
1. **Call a coordinate**: Announce one unused square clearly (e.g., "Fire at H6").
2. **Resolve the shot**: The defender checks their ocean grid and answers "miss" (empty) or "hit" (unhit ship segment).
3. **Record the result**: Attacker marks the targeting grid; defender marks the ocean grid (e.g., X for hit, O/dot for miss).
4. **Announce a sinking**: If the shot hits the final intact segment, the defender names the ship (e.g., "You sank my Destroyer").
5. **End the turn**: Play passes to the opponent.

## 4. Hits, Misses, and Sunk Ships
- A shot is resolved strictly against the exact coordinate called; nearby ships do not trigger a hit. A damaged ship remains in its position until every square belonging to it has been hit.
- The defender must report truthfully and promptly, naming sunk ships under standard rules. Unhit segments are kept secret.

## 5. Optional Playing Modes
- **Salvo mode**: Players call a number of coordinates equal to their surviving ships at the start of the turn.
- **Fixed three-shot mode (Easier)**: Each player calls three different coordinates per turn regardless of surviving ships, with full hit/sink feedback.
- **Fixed three-shot mode (Harder)**: Attacker calls three coordinates, and the defender reports only the total number of hits (e.g., "two hits") without specifying which coordinates hit.
- **No-touch fleet variant**: Ships may not occupy adjacent squares horizontally, vertically, or diagonally.

## 6. Edge Cases and Official Table Rulings
- **Repeated coordinate**: If noticed before the defender answers, choose another square. If already answered, it counts as a wasted turn.
- **Invalid coordinate**: A call outside A-J or 1-10 must be corrected immediately.
- **Two ships touching**: A hit at a boundary belongs exclusively to the exact square occupied by that specific ship.
- **Illegal setup found late**: Under strict play, the owner forfeits; in friendly games, pause and redeploy legally.

## 7. End of the Game
- The game ends immediately when every segment of all enemy ships has been hit. The attacker who destroys the final ship wins.

## 8. Search Strategy - Finding the First Hit
- **Use parity instead of random shots**: Fire primarily on one color of a mental checkerboard pattern, since every ship of length 2 or more must intersect it.
- **Prefer high-probability squares**: Central squares cover more potential ship placements than corners early in the game.

## 9. Target Strategy - Converting a Hit into a Sink
- After a hit, test the four orthogonally adjacent squares (left, right, above, below). Once a second aligned hit confirms orientation, continue along both ends of the line.

## 10. Deployment Tricks and Defensive Tips
- Avoid obvious symmetry or placing all ships on edges. Mix orientations, separate some ships to prevent clustered hits, and keep your physical reactions neutral when hit.

## 11. Common Mistakes to Avoid
- Failing to mark misses, continuing search mode after a hit, guessing diagonally, assuming a ship sank before announcement, and changing house rules mid-game.

## 12. Quick Reference Checklist
- Summary of pre-game verifications, turn actions, and sink protocols.