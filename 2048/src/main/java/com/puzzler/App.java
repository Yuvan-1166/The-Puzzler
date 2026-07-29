package com.puzzler;

public class App {
    public static void main(String[] args) {
        System.out.println("The Puzzler!");

        Game game = new Game();
        game.gameLoop();
    }
}
