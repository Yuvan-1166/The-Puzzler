package com.puzzler.dto;

public class BoardDTO {

  private int[][] board;
  private int score;
  private boolean isGameOver;

  public BoardDTO (int[][] board, int score, boolean isGameOver) {
    this.board = board;
    this.score = score;
    this.isGameOver = isGameOver;
  }

}
