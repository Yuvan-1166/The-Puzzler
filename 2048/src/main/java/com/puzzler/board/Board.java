package com.puzzler.board;

import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

public class Board {

  private static final int[][] directions = new int[][] {{1,0},{-1,0},{0,1},{0,-1}};
  private int[][] board;
  private int[][] prevState;
  private int score;

  public Board () {
    init();
  }

  public void init() {
    this.board = new int[4][4];
    this.prevState = new int[4][4];
    this.score = 0;
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

  private void spawnNext() {
    List<int[]> emptyCell = new ArrayList<>();
    for(int i=0;i<4;i++) {
      for(int j=0;j<4;j++) {
        if(board[i][j] == 0)
          emptyCell.add(new int[] {i, j});
      }
    }
    if(emptyCell.isEmpty() || !isChanged())
      return;
    int x = ThreadLocalRandom.current().nextInt(emptyCell.size());

    int[] pos = emptyCell.get(x);
    board[pos[0]][pos[1]] = ThreadLocalRandom.current().nextInt(10) == 0 ? 4 : 2;
    
    for(int i=0;i<4;i++)
      prevState[i] = Arrays.copyOf(board[i], 4);
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

  private boolean isChanged() {
    return !Arrays.deepEquals(board, prevState);
  }

  private void compress(int[] line) {
    for(int i=1;i<4;i++) {
      int j = i-1;
      while(j >= 0 && line[j] == 0) {
        line[j] = line[j+1];
        line[j+1] = 0;
        j--;
      }
    }
  }

  private void merge(int[] line) {
    for(int i=1;i<4;i++) {
      if(line[i] != 0 && line[i] == line[i-1]) {
        line[i-1] *= 2;
        line[i] = 0;
        score += line[i-1];
      }
    }
  }

  public void leftMove() {
    for(int i=0;i<4;i++) {
      compress(board[i]);
      merge(board[i]);
      compress(board[i]);
    }
    spawnNext();
  }

  public void rightMove() {
    for(int i=0;i<4;i++) {
      int[] line = new int[4];
      for(int j=0;j<4;j++)
        line[3-j] = board[i][j];
      compress(line);
      merge(line);
      compress(line);
      for(int j=0;j<4;j++)
        board[i][j] = line[3-j];
    }
    spawnNext();
  }

  public void upMove() {
    for(int i=0;i<4;i++) {
      int[] line = new int[4];
      for(int j=0;j<4;j++)
        line[j] = board[j][i];
      compress(line);
      merge(line);
      compress(line);
      for(int j=0;j<4;j++) 
        board[j][i] = line[j];
    }
    spawnNext();
  }

  public void downMove() {
    for(int i=0;i<4;i++) {
      int[] line = new int[4];
      for(int j=0;j<4;j++) 
        line[3-j] = board[j][i];
      compress(line);
      merge(line);
      compress(line);
      for(int j=0;j<4;j++) 
        board[j][i] = line[3-j];
    }
    spawnNext();
  }

  public String toString() {
    StringBuilder grid = new StringBuilder();
    grid.append("2048\nScore: ").append(score).append('\n');
    for(int[] row : board)
      grid.append(Arrays.toString(row)).append("\n");
    return grid.toString();
  }

}
