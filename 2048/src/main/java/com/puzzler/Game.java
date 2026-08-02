package com.puzzler;

import java.util.*;
import com.puzzler.board.Board;
import com.puzzler.utils.Util;

public class Game {

  private Board board;
  Scanner scan;

  public Game() {
    this.board = new Board();
    scan = new Scanner(System.in);
  }

  public boolean gameLoop() {

    while(true) {
      Util.clearScreen();
      System.out.println(board);
      System.out.println("WASD - Direction\nq - quit\n");
      char x = Character.toUpperCase(scan.next().charAt(0));
      boolean breakLoop = false;
      if(!board.isMoveAvailable())
        return false;
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
        case 'Q':
          breakLoop = true;
          break;
        default:
          System.out.println("Invalid Move");
          break;
      }
      if(breakLoop)
        break;
    }

    return true;
  }

}
