// Create the 9x9 Sudoku grid dynamically
window.onload = function() {
    const board = document.getElementById("sudoku-board");
    for (let i = 0; i < 81; i++) {
        const input = document.createElement("input");
        input.type = "text";
        input.maxLength = 1;
        input.oninput = () => {
            // Ensure only digits 1-9 are accepted
            input.value = input.value.replace(/[^1-9]/g, '');
        };
        board.appendChild(input);
    }
};

// Helper to get current board values as a 2D array
function getBoardValues() {
    const inputs = document.querySelectorAll("#sudoku-board input");
    let board = [];
    for (let i = 0; i < 9; i++) {
        let row = [];
        for (let j = 0; j < 9; j++) {
            const val = inputs[i * 9 + j].value;
            row.push(val === "" ? 0 : parseInt(val));
        }
        board.push(row);
    }
    return board;
}

// Helper to update the board display with solved values
function updateBoard(board) {
    const inputs = document.querySelectorAll("#sudoku-board input");
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            inputs[i * 9 + j].value = board[i][j] === 0 ? "" : board[i][j];
        }
    }
}

// Validate initial board for conflicts
function isValidBoard(board) {
    for (let i = 0; i < 9; i++) {
        let rowSet = new Set();
        let colSet = new Set();
        let boxSet = new Set();
        for (let j = 0; j < 9; j++) {
            // Row check
            if (board[i][j] !== 0) {
                if (rowSet.has(board[i][j])) return false;
                rowSet.add(board[i][j]);
            }
            // Column check
            if (board[j][i] !== 0) {
                if (colSet.has(board[j][i])) return false;
                colSet.add(board[j][i]);
            }
            // Box check
            let rowIndex = 3 * Math.floor(i / 3) + Math.floor(j / 3);
            let colIndex = 3 * (i % 3) + (j % 3);
            if (board[rowIndex][colIndex] !== 0) {
                if (boxSet.has(board[rowIndex][colIndex])) return false;
                boxSet.add(board[rowIndex][colIndex]);
            }
        }
    }
    return true;
}

// Solve puzzle using backtracking algorithm
function solveSudoku() {
    let board = getBoardValues();
    const message = document.getElementById("message");
    message.textContent = "";

    if (!isValidBoard(board)) {
        message.textContent = "Invalid puzzle: conflicting numbers detected.";
        return;
    }

    if (solve(board)) {
        updateBoard(board);
        message.textContent = "Puzzle solved successfully!";
    } else {
        message.textContent = "No solution exists for this puzzle.";
    }
}

// Backtracking solver
function solve(board) {
    let empty = findEmpty(board);
    if (!empty) return true;

    let [row, col] = empty;
    for (let num = 1; num <= 9; num++) {
        if (isValidMove(board, row, col, num)) {
            board[row][col] = num;
            if (solve(board)) return true;
            board[row][col] = 0;
        }
    }
    return false;
}

// Find first empty cell
function findEmpty(board) {
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            if (board[i][j] === 0) return [i, j];
        }
    }
    return null;
}

// Check if placing number is valid
function isValidMove(board, row, col, num) {
    for (let i = 0; i < 9; i++) {
        if (board[row][i] === num || board[i][col] === num) return false;
        let boxRow = 3 * Math.floor(row / 3) + Math.floor(i / 3);
        let boxCol = 3 * Math.floor(col / 3) + (i % 3);
        if (board[boxRow][boxCol] === num) return false;
    }
    return true;
}

// Clear the board
function clearBoard() {
    const inputs = document.querySelectorAll("#sudoku-board input");
    inputs.forEach(input => input.value = "");
    document.getElementById("message").textContent = "";
}
