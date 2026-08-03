package com.puzzler;

import java.util.*;
import com.google.gson.Gson;
import com.puzzler.dto.InputDTO;
import com.puzzler.board.Board;
import com.puzzler.utils.Util;

public class Game {

  private static final Gson gson = new Gson();
  private Board board;
  Scanner scan;

  public Game() {
    this.board = new Board();
    scan = new Scanner(System.in);
  }

  public boolean gameLoop() {
    while(true) {
      if(!board.isMoveAvailable())
        board.setIsGameOver();

      System.out.println(board);

      String input = scan.nextLine();
      InputDTO inputDTO = gson.fromJson(input, InputDTO.class);

      char x = Character.toUpperCase(inputDTO.getMove());
      boolean breakLoop = false;

      switch(x) {
        case 'W':
          board.upMove();
          break;
        case 'A':
          board.leftMove();
          break;
        case 'S':
          board.downMove();
          break;
        case 'D':
          board.rightMove();
          break;
        case 'R':
          board.init();
          break;
        case 'Q':
          breakLoop = true;
      }
      if(breakLoop)
        break;
    }

    return true;
  }

}
