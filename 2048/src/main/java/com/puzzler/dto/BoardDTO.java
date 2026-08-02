package com.puzzler.dto;

public class BoardDTO {

  private int[][] board;
  private int score;

  public BoardDTO (int[][] board, int score) {
    this.board = board;
    this.score = score;
  }

}
