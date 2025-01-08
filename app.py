import streamlit as st
import streamlit.components.v1 as components

# HTML과 JavaScript를 포함한 테트리스 코드
html_code = """
<!DOCTYPE html>
<html>
<head>
    <title>Tetris Game</title>
    <style>
        body { text-align: center; color: white; background-color: black; }
        canvas { background: #000; display: block; margin: 0 auto; }
        .button { border-radius: 50%; width: 80px; height: 80px; font-size: 20px; cursor: pointer; margin: 5px; }
        .start { background-color: red; color: white; }
        .exit { background-color: blue; color: white; }
        .replay { background-color: green; color: white; }
        #score { font-size: 20px; margin-top: 10px; }
    </style>
</head>
<body>
    <div id="score">Score: 0</div>
    <canvas id="gameCanvas" width="320" height="640"></canvas>
    <br>
    <div>
        <button class="button start" onclick="startGame()">Start</button>
        <button class="button replay" onclick="replayGame()" style="display: none;">Replay</button>
        <button class="button exit" onclick="exitGame()">Exit</button>
    </div>
    <script>
        let canvas = document.getElementById('gameCanvas');
        let context = canvas.getContext('2d');
        let grid = 32;
        let tetrominoes = [
            [[1, 1, 1], [0, 1, 0]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 1, 0], [0, 1, 1]],
            [[1, 0, 0], [1, 1, 1]],
            [[0, 0, 1], [1, 1, 1]],
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]]
        ];
        let rAF = null; // Animation frame request ID
        let tetromino = null; // Current tetromino
        let nextTetromino = null; // Next tetromino
        let tetrominoX = 0; // Current tetromino X coordinate
        let tetrominoY = 0; // Current tetromino Y coordinate
        let board = []; // Game board
        let dropInterval = null; // Interval for dropping tetromino
        let score = 0; // Player's score

        function resetGame() {
            board = Array.from({ length: 20 }, () => Array(10).fill(0));
            nextTetromino = getNextTetromino();
            spawnTetromino();
            score = 0;
            updateScore();
        }

        function getNextTetromino() {
            const index = Math.floor(Math.random() * tetrominoes.length);
            return tetrominoes[index];
        }

        function spawnTetromino() {
            tetromino = nextTetromino;
            nextTetromino = getNextTetromino();
            tetrominoX = Math.floor((10 - tetromino[0].length) / 2);
            tetrominoY = 0;
        }

        function drawTetromino() {
            context.fillStyle = 'red';
            tetromino.forEach((row, y) => {
                row.forEach((value, x) => {
                    if (value) {
                        context.fillRect((tetrominoX + x) * grid, (tetrominoY + y) * grid, grid, grid);
                    }
                });
            });
        }

        function drawBoard() {
            context.clearRect(0, 0, canvas.width, canvas.height);
            board.forEach((row, y) => {
                row.forEach((value, x) => {
                    if (value) {
                        context.fillStyle = 'blue';
                        context.fillRect(x * grid, y * grid, grid, grid);
                    }
                });
            });
        }

        function updateGame() {
            tetrominoY++;
            if (collision()) {
                tetrominoY--;
                mergeTetromino();
                clearLines();
                if (gameOver()) {
                    cancelAnimationFrame(rAF);
                    clearInterval(dropInterval);
                    return;
                } else {
                    spawnTetromino();
                }
            }
        }

        function collision() {
            for (let y = 0; y < tetromino.length; y++) {
                for (let x = 0; x < tetromino[y].length; x++) {
                    if (tetromino[y][x] && (board[tetrominoY + y] && board[tetrominoY + y][tetrominoX + x]) !== 0) {
                        return true;
                    }
                }
            }
            return false;
        }

        function mergeTetromino() {
            tetromino.forEach((row, y) => {
                row.forEach((value, x) => {
                    if (value) {
                        board[tetrominoY + y][tetrominoX + x] = value;
                    }
                });
            });
        }

        function clearLines() {
            let linesCleared = 0;
            board = board.filter(row => {
                if (row.every(value => value !== 0)) {
                    linesCleared++;
                    return false;
                }
                return true;
            });
            while (board.length < 20) {
                board.unshift(Array(10).fill(0));
            }
            score += linesCleared * 10;
            updateScore();
        }

        function updateScore() {
            document.getElementById('score').innerText = 'Score: ' + score;
        }

        function gameOver() {
            return board[0].some(value => value !== 0);
        }

        function gameLoop() {
            drawBoard();
            drawTetromino();
            rAF = requestAnimationFrame(gameLoop);
        }

        function rotateTetromino() {
            const rotated = tetromino[0].map((_, index) => tetromino.map(row => row[index])).reverse();
            const originalX = tetrominoX;
            const originalY = tetrominoY;
            tetrominoX = Math.min(Math.max(tetrominoX, 0), 10 - rotated[0].length);
            tetrominoY = Math.min(Math.max(tetrominoY, 0), 20 - rotated.length);
            if (!collision()) {
                tetromino = rotated;
            } else {
                tetrominoX = originalX;
                tetrominoY = originalY;
            }
        }

        function startGame() {
            canvas.style.display = 'block';
            document.querySelector('.start').style.display = 'none';
            document.querySelector('.replay').style.display = 'inline-block';
            resetGame();
            gameLoop();
            dropInterval = setInterval(updateGame, 1000); // Drop tetromino every 1 second
        }

        function replayGame() {
            exitGame();
            startGame();
        }

        function exitGame() {
            cancelAnimationFrame(rAF);
            clearInterval(dropInterval);
            canvas.style.display = 'none';
            document.querySelector('.start').style.display = 'inline-block';
            document.querySelector('.replay').style.display = 'none';
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') {
                tetrominoX--;
                if (collision()) {
                    tetrominoX++;
                }
            } else if (e.key === 'ArrowRight') {
                tetrominoX++;
                if (collision()) {
                    tetrominoX--;
                }
            } else if (e.key === 'ArrowDown') {
                tetrominoY++;
                if (collision()) {
                    tetrominoY--;
                }
            } else if (e.key === 'ArrowUp') {
                rotateTetromino();
            }
        });
    </script>
</body>
</html>
"""

st.title('Tetris Game')

# HTML 및 JavaScript 포함
components.html(html_code, height=800)
