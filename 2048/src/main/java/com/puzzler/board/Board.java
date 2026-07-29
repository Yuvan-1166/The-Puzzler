package com.puzzler.board;

import java.util.Arrays;
import java.util.concurrent.ThreadLocalRandom;

public class Board {

  private int[][] board;

  public Board () {
    this.board = new int[4][4];
  }

  public void init() {
    int[] pos1 = generateRandomPosition();
    int[] pos2 = generateRandomPosition();

    while(Arrays.equals(pos1, pos2))
      pos2 = generateRandomPosition();

    board[pos1[0]][pos1[1]] = ThreadLocalRandom.current().nextInt(10) == 0 ? 4 : 2;
    board[pos2[0]][pos2[1]] = ThreadLocalRandom.current().nextInt(10) == 0 ? 4 : 2;
  }

  private int[] generateRandomPosition() {
    int x = ThreadLocalRandom.current().nextInt(4);
    int y = ThreadLocalRandom.current().nextInt(4);
    return new int[] {x, y};
  }

  public String toString() {
    StringBuilder grid = new StringBuilder();
    for(int[] row : board)
      grid.append(Arrays.toString(row)).append("\n");
    return grid.toString();
  }

}
