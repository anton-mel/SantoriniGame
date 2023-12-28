# Anton Melnychuk & Oliver Li

from tkinter import StringVar
import tkinter as tk

class SantoriniCLI:
    """Client Interaction Helper Functions."""
    
    def __init__(self):
        self.result = None

    def select_worker(self):
        """Prompts the user to select a worker and returns the input."""
        worker_frame = tk.Toplevel()
        worker_frame.title("Select Worker")

        label = tk.Label(worker_frame, text="Select a worker to move (A, B, Y, Z):")
        label.pack(pady=10)

        entry_var = tk.StringVar()
        entry = tk.Entry(worker_frame, textvariable=entry_var)
        entry.pack(pady=10)

        ok_button = tk.Button(worker_frame, text="OK", command=lambda: worker_frame.destroy())
        ok_button.pack(pady=10)

        worker_frame.wait_window(worker_frame)

        selected_worker = entry_var.get().upper()
        valid_workers = ["A", "B", "Y", "Z"]
        
        self.undoredo = None
        self.result_variable = tk.StringVar()

        if selected_worker not in valid_workers:
            raise ValueError("Not a valid worker")

        return selected_worker

    def get_direction(self, prompt):
        """
        Prompts the user to input a direction and validates it.
        Returns the validated direction.
        """

        while True:
            direction_frame = tk.Toplevel()
            direction_frame.title("Enter Direction")

            label = tk.Label(direction_frame, text=prompt)
            label.pack(pady=10)

            entry_var = tk.StringVar()
            entry = tk.Entry(direction_frame, textvariable=entry_var)
            entry.pack(pady=10)

            ok_button = tk.Button(direction_frame, text="OK", command=lambda: direction_frame.destroy())
            ok_button.pack(pady=10)

            direction_frame.wait_window(direction_frame)

            direction = entry_var.get().lower()
            valid_directions = ("n", "ne", "e", "se", "s", "sw", "w", "nw")

            if direction not in valid_directions:
                self.print_direction_error("Not a valid direction")
            else:
                return direction
    
    def get_memento(self, root):
        result_var = tk.StringVar()

        if not hasattr(root, "_frame_buttons"):
            frame_buttons = tk.Frame(root)
            frame_buttons.pack(fill="x", expand=True)
            root._frame_buttons = frame_buttons

            button_types = ["undo", "redo", "next"]
            for button_type in button_types:
                button = tk.Button(frame_buttons, text=button_type, command=lambda b=button_type: self.set_result(b, result_var))
                button.pack(side=tk.LEFT, padx=20)
                setattr(frame_buttons, f"{button_type.lower()}_button", button)
        else:
            for button_type in ["undo", "redo", "next"]:
                button = getattr(root._frame_buttons, f"{button_type.lower()}_button", None)
                if button:
                    button.configure(command=lambda b=button_type: self.set_result(b, result_var))

        root.wait_variable(result_var)
        return result_var.get()

    def set_result(self, value, result_var):
        result_var.set(value)
        # Your additional logic here

    def get_move(self):
        prompt = "Select a direction to move (n, ne, e, se, s, sw, w, nw)\n"
        return self.get_direction(prompt)

    def get_build(self):
        prompt = "Select a direction to build (n, ne, e, se, s, sw, w, nw)\n"
        return self.get_direction(prompt)

    def print_board(self, board, root):
        board.__repr__(root)

    def print_score(self, h_score, c_score, d_score, root):
        score_text = f"Cell Height ({h_score}), Grid Scrore ({c_score}), Distance (AI) ({d_score})"
        
        if not hasattr(self, "_frame_score"):
            # Create a frame with green background and full width
            self._frame_score = tk.Frame(root, bg="#b3ffb3")
            self._frame_score.pack(fill="x", expand=True)

            # Create a label inside the frame
            self._label_score = tk.Label(self._frame_score, text="", bg="#b3ffb3", fg="#000")
            self._label_score.pack()

        # Update the label's text
        self._label_score.config(text=score_text)

    def print_invalid_move(self, e):
        # Create a Toplevel window for the alert
        alert_window = tk.Toplevel()

        # Configure the Toplevel window
        alert_window.configure(bg="red")
        alert_window.title("Error Alert")

        # Create a label inside the Toplevel window
        error_message = f"Cannot {e.move_type} {e.direction}"
        label_alert = tk.Label(alert_window, text=error_message, bg="red", fg="white")
        label_alert.pack(padx=10, pady=10)

        # Schedule the Toplevel window to be destroyed after a certain time (e.g., 2000 milliseconds)
        alert_window.after(4000, alert_window.destroy)

    def print_worker_error(self, mes):
        # Create a Toplevel window for the alert
        alert_window = tk.Toplevel()

        # Configure the Toplevel window
        alert_window.configure(bg="red")
        alert_window.title("Error Alert")

        # Create a label inside the Toplevel window
        label_alert = tk.Label(alert_window, text=mes, bg="red", fg="white")
        label_alert.pack(padx=10, pady=10)

        # Schedule the Toplevel window to be destroyed after a certain time (e.g., 2000 milliseconds)
        alert_window.after(4000, alert_window.destroy)

    def print_turn(self, turn, color, workers, root):
        turn_text = f"Turn: {turn}, {color} ({workers})"
        
        if not hasattr(self, "_frame_turn"):
            # Create a frame with blue background and full width
            self._frame_turn = tk.Frame(root, bg="#f9f9f9")
            self._frame_turn.pack(fill="x", expand=True)

            # Create a label inside the frame
            self._label_turn = tk.Label(self._frame_turn, text="", bg="#f9f9f9", fg="#000")
            self._label_turn.pack()

        # Update the label's text
        self._label_turn.config(text=turn_text)

    def print_end(self, restart, winner, root):
        """Prints the end of the game, including the winner, and prompts for a restart by passing the function."""

        # Create a custom popup frame
        end_frame = tk.Toplevel()
        end_frame.title("Game Over")

        # Add labels and buttons to the frame
        label = tk.Label(end_frame, text=f"{winner} has won! Play again?")
        label.pack(pady=10)

        yes_button = tk.Button(end_frame, text="Yes", command=lambda: self.handle_play_again(end_frame, restart))
        yes_button.pack(side=tk.LEFT, padx=10)

        no_button = tk.Button(end_frame, text="No", command=lambda: self.handle_exit(end_frame, root))
        no_button.pack(side=tk.RIGHT, padx=10)
        
        end_frame.wait_window(end_frame)

    def handle_play_again(self, frame, restart):
        # Destroy the popup frame and restart the game
        frame.destroy()
        restart()

    def handle_exit(self, frame, root):
        # Destroy the popup frame and exit the program
        frame.destroy()
        root.destroy()
        root.quit()
        
    def last(self, symbol, move, build, root):
        last_move_text = f"Last Move: {symbol}, Move: {move}, Build: {build}"
        
        if not hasattr(self, "_frame_last_move"):
            # Create a frame with yellow background and full width
            self._frame_last_move = tk.Frame(root, bg="#ffffb3")
            self._frame_last_move.pack(fill="x", expand=True)

            # Create a label inside the frame
            self._label_last_move = tk.Label(self._frame_last_move, text="", bg="#ffffb3", fg="#000")
            self._label_last_move.pack()

        # Update the label's text
        self._label_last_move.config(text=last_move_text)

s_cli = SantoriniCLI()


def parse_args():
    root = tk.Tk()
    root.geometry("600x420")
    root.resizable(False, False)
    root.title("Santorini Game Configuration")

    white_player_type_var = StringVar(value="human")
    blue_player_type_var = StringVar(value="human")
    undo_redo_var = StringVar(value="off")
    score_display_var = StringVar(value="off")

    def on_ok():
        root.destroy()

    # Player Types
    tk.Label(root, text="White Player Type:").pack(pady=5)
    white_player_types = [("Human", "human"), ("Random", "random"), ("Heuristic", "heuristic")]
    for text, value in white_player_types:
        tk.Radiobutton(root, text=text, variable=white_player_type_var, value=value).pack()

    tk.Label(root, text="Blue Player Type:").pack(pady=5)
    blue_player_types = [("Human", "human"), ("Random", "random"), ("Heuristic", "heuristic")]
    for text, value in blue_player_types:
        tk.Radiobutton(root, text=text, variable=blue_player_type_var, value=value).pack()

    # Undo/Redo
    tk.Label(root, text="Undo/Redo:").pack(pady=5)
    undo_redo_options = [("On", "on"), ("Off", "off")]
    for text, value in undo_redo_options:
        tk.Radiobutton(root, text=text, variable=undo_redo_var, value=value).pack()

    # Score Display
    tk.Label(root, text="Score Display:").pack(pady=5)
    score_display_options = [("On", "on"), ("Off", "off")]
    for text, value in score_display_options:
        tk.Radiobutton(root, text=text, variable=score_display_var, value=value).pack()

    # OK Button
    tk.Button(root, text="OK", command=on_ok).pack(pady=10)

    root.mainloop()

    return {
        "white": white_player_type_var.get(),
        "blue": blue_player_type_var.get(),
        "undo_redo": undo_redo_var.get(),
        "score_display": score_display_var.get(),
    }
