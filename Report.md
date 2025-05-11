---
title: "HexaPawn: A Strategic Variant with Enhanced AI"
---

Submitted By: 19K-0337 Shahzaib

Course: AI

Instructor: Talha Shahid

Submission Date: May 11, 2025

# 1. Executive Summary

This project presents a strategic variant of the classical HexaPawn
game, implemented on a 4x4 board. It introduces a new \"blocker\" piece
and a push mechanic, significantly increasing the complexity and
strategic depth of the game. A custom AI opponent was developed using
the Minimax algorithm enhanced with Alpha-Beta pruning and a heuristic
evaluation function focusing on mobility, positioning, and material
balance.

# 2. Introduction

## Background:

HexaPawn is a simplified chess variant designed by Martin Gardner,
originally played on a 3x3 board with pawns. The goal is to reach the
opponent's back row or capture all enemy pawns. The game was selected
for its simplicity and potential for strategic enhancement.

## Objectives of the Project:

\- Extend HexaPawn to a 4x4 board.\
- Add new gameplay features (blockers and push mechanics).\
- Develop an AI that can strategically play the enhanced game using
Minimax and Alpha- Beta pruning.\
- Evaluate AI performance in terms of decision time and win rate.

# 3. Game Description

## Original Game Rules:

\- 3x3 board with 3 pawns per player.\
- Pawns move forward and capture diagonally.\
- Win by reaching the opponent's back row or capturing all enemy pawns.

## Innovations and Modifications:

\- 4x4 board with 4 pawns and 1 blocker per player.\
- Blocker: An immobile piece that obstructs opponent pawns.\
- Push mechanic: Two adjacent pawns can remove a blocker.\
- Increased branching factor (\~8 vs. 4).\
- Enhanced strategic gameplay requiring deeper planning.

# 4. AI Approach and Methodology

## AI Techniques Used:

Minimax algorithm with Alpha-Beta pruning (search depth: 4).

## Algorithm and Heuristic Design:

\- Evaluation Function:\
- Pawn = 1 point, Blocker = 2 points.\
- Positional bonus for center control and proximity to promotion row.\
- Mobility score based on the number of legal moves.\
- Bonuses for controlling back row.

## AI Performance Evaluation:

\- Average decision-making time kept under 2 seconds per move.\
- Demonstrated high win rate against casual human players in testing.

# 5. Game Mechanics and Rules

## Modified Game Rules:

\- Each player starts with 4 pawns and 1 blocker.\
- Blockers begin in the second row.\
- Blockers are immobile but can be removed via a push.\
- Push rule requires two aligned allied pawns.

## Turn-based Mechanics:

\- Alternate turns between the human player (white) and AI (black).\
- On each turn, a pawn may move, capture, or push a blocker.

## Winning Conditions:

\- A player wins by:\
- Reaching the opponent's back row.\
- Eliminating all opponent pawns.

# 6. Implementation and Development

## Development Process:

Implemented in Python using Pygame for GUI. Minimax algorithm designed
from scratch with recursive calls and pruning. Evaluation function
finely tuned for enhanced decision-making.

## Programming Languages and Tools:

\- Language: Python\
- Libraries: Pygame, NumPy\
- Tools: Manual testing, Python IDLE

## Challenges Encountered:

\- Designing and debugging the push mechanic.\
- Optimizing AI performance to maintain low decision latency.\
- Balancing heuristic weights for consistent AI behavior.

# 7. Team Contributions

Since this was an individual project:\
- Shahzaib (19K-0337): Handled complete design and implementation,
including game mechanics, GUI, AI development, and testing.

# 8. Results and Discussion

## AI Performance:

\- Achieved stable AI performance with decisions made in under 2
seconds.\
- Win rate above 90% in informal testing scenarios.\
- Demonstrated strategic depth and effective use of new game mechanics.

# 9. References

1\. Russell & Norvig, Artificial Intelligence: A Modern Approach
(Minimax, Alpha-Beta).\
2. Martin Gardner -- Original HexaPawn rules.\
3. Pygame Documentation -- https://www.pygame.org/docs/
