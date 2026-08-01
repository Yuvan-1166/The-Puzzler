package com.puzzler.board;

import java.util.Arrays;
import java.util.concurrent.ThreadLocalRandom;

public class Board {

  private static final int[][] directions = new int[][] {{1,0},{-1,0},{0,1},{0,-1}};
  private int[][] board;
  private int score;

  public Board () {
    this.board = new int[4][4];
    this.score = 0;
  }

  public void init() {
    int[] pos1 = generateRandomPosition();
    int[] pos2 = generateRandomPosition();

    while(Arrays.equals(pos1, pos2))
      pos2 = generateRandomPosition();

    board[pos1[0]][pos1[1]] = ThreadLocalRandom.current().nextInt(10) == 0 ? 4 : 2;
    board[pos2[0]][pos2[1]] = ThreadLocalRandom.current().nextInt(10) == 0 ? 4 : 2;

    score += (board[pos1[0]][pos1[1]] + board[pos2[0]][pos2[1]]);
  }

  private int[] generateRandomPosition() {
    int x = ThreadLocalRandom.current().nextInt(4);
    int y = ThreadLocalRandom.current().nextInt(4);
    return new int[] {x, y};
  }

  public boolean isMoveAvailable() {
    for(int i=0;i<4;i++) {
      for(int j=0;j<4;j++) {
        if(board[i][j] == 0)
          return true;
        for(int[] dir : directions) {
          int x = i + dir[0];
          int y = j + dir[1];

          if(x < 0 || x > 3 || y < 0 || y > 3)
            continue;
          if(board[i][j] == board[x][y])
            return true;
        }
      }
    }
    return false;
  }

  public String toString() {
    StringBuilder grid = new StringBuilder();
    for(int[] row : board)
      grid.append(Arrays.toString(row)).append("\n");
    return grid.toString();
  }

}
