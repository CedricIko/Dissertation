# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bxBluDwoWn29GmHLXtEVCi6Jukl7im0g
"""

import streamlit as st
import chess
import chess.svg
from making_predictions import find_best_move  # Import your model-based move function

# Initialize the game state
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
    st.session_state.move_log = []
    st.session_state.player_color = "White"
    st.session_state.awaiting_ai_move = False

st.title("Play Chess Against Minimax AI")
player_color = st.radio("Choose your color", ("White", "Black"))
st.session_state.player_color = player_color

# Render and display the chessboard using raw SVG embedding
def render_svg(board):
    svg_data = chess.svg.board(board=board)
    return f'<div style="width: 400px;">{svg_data}</div>'

# Display initial board
#board_slot = st.empty()  # Slot to dynamically update the board
st.components.v1.html(render_svg(st.session_state.board), height=450)

# AI move handling for Black AI start
if len(st.session_state.move_log) == 0 and player_color == "Black": #and not st.session_state.awaiting_ai_move:
    ai_move = find_best_move(st.session_state.board, depth=3)
    if isinstance(ai_move, str):  # Check if the move is a string
        ai_move = chess.Move.from_uci(ai_move)  # Convert UCI string to Move object
    if ai_move and ai_move in st.session_state.board.legal_moves:
        st.session_state.board.push(ai_move)
        st.session_state.move_log.append(f"AI (White): {ai_move.uci()}")
        #board_slot.html(render_svg(st.session_state.board))
        st.rerun()
# Create a form for the player's move input
with st.form(key="player_move_form"):
    move = st.text_input("Enter your move in UCI format (e.g., e2e4):")
    submit_button = st.form_submit_button(label="Submit Move")

# Handle player's move and update board
if submit_button and move:
    player_move = chess.Move.from_uci(move)
    if player_move in st.session_state.board.legal_moves:
        st.session_state.board.push(player_move)
        st.session_state.move_log.append(f"Player ({player_color}): {move}")

        # Update board after player's move
        #board_slot.html(render_svg(st.session_state.board))

        st.session_state.awaiting_ai_move = True  # Flag to trigger AI's move next rerun
        st.rerun()
        # Check if the game is over after the player's move
        if st.session_state.board.is_game_over():
            st.write("Game over!")
            st.stop()
    else:
        st.write("Invalid move. Please try again.")

# Handle AI's move after player's move
if st.session_state.awaiting_ai_move and not st.session_state.board.is_game_over():
    ai_move = find_best_move(st.session_state.board, depth=7)
    if isinstance(ai_move, str):  # Convert to Move object if needed
        ai_move = chess.Move.from_uci(ai_move)
    if ai_move and ai_move in st.session_state.board.legal_moves:
        st.session_state.board.push(ai_move)
        st.session_state.move_log.append(f"AI ({'Black' if player_color == 'White' else 'White'}): {ai_move.uci()}")
        st.session_state.awaiting_ai_move = False  # Reset flag after AI's move
        st.rerun()
        # Update board after AI's move
        #board_slot.html(render_svg(st.session_state.board))
        # Check if the game is over after the AI's move
        if st.session_state.board.is_game_over():
            st.write("Game over!")

# Display move log
st.write("Move log:")
for move in st.session_state.move_log:
    st.write(move)

# Restart game functionality
if st.button("Restart Game"):
    for key in ["board", "move_log", "player_color", "awaiting_ai_move"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

