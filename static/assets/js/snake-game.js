var canvas = document.createElement('canvas');
var ctx = canvas.getContext('2d');
canvas.width = 600;
canvas.height = 400;
document.getElementById('snake-game').appendChild(canvas);

var tileSize = 20;
var tileCountX = Math.floor(canvas.width / tileSize);
var tileCountY = Math.floor(canvas.height / tileSize);
var snake = [{x: 10, y: 10}];
var food = {x: 15, y: 15};
var dx = 0;
var dy = 0;
var score = 0;


function main() {
    update();
    draw();
    requestAnimationFrame(main);
}

function update() {
    if (checkCollision()) {
        resetGame();
    }

    var head = {x: snake[0].x + dx, y: snake[0].y + dy};
    snake.unshift(head);

    if (head.x === food.x && head.y === food.y) {
        score++;
        generateFood();
    } else {
        snake.pop();
    }
}

function checkCollision() {
    var head = snake[0];
    return (
        head.x < 0 ||
        head.x >= tileCountX ||
        head.y < 0 ||
        head.y >= tileCountY ||
        snake.slice(1).some(segment => segment.x === head.x && segment.y === head.y)
    );
}

function resetGame() {
    snake = [{x: 10, y: 10}];
    dx = 0;
    dy = 0;
    score = 0;
    generateFood();
}

function generateFood() {
    food.x = Math.floor(Math.random() * tileCountX);
    food.y = Math.floor(Math.random() * tileCountY);
}

function draw() {
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = 'lime';
    snake.forEach(segment => {
        ctx.fillRect(segment.x * tileSize, segment.y * tileSize, tileSize, tileSize);
    });

    ctx.fillStyle = 'red';
    ctx.fillRect(food.x * tileSize, food.y * tileSize, tileSize, tileSize);

    ctx.fillStyle = 'white';
    ctx.font = '20px Arial';
    ctx.fillText('Score: ' + score, 10, 30);
}

document.addEventListener('keydown', function (event) {
    if (event.key === 'ArrowUp' && dy === 0) {
        dx = 0;
        dy = -1;
    } else if (event.key === 'ArrowDown' && dy === 0) {
        dx = 0;
        dy = 1;
    } else if (event.key === 'ArrowLeft' && dx === 0) {
        dx = -1;
        dy = 0;
    } else if (event.key === 'ArrowRight' && dx === 0) {
        dx = 1;
        dy = 0;
    }
});

document.addEventListener('keydown', function (event) {
    if (isPlaying && ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(event.key)) {
        event.preventDefault();
    }

    if (isPlaying) {
        if (event.key === 'ArrowUp' && dy === 0) {
            dx = 0;
            dy = -1;
        } else if (event.key === 'ArrowDown' && dy === 0) {
            dx = 0;
            dy = 1;
        } else if (event.key === 'ArrowLeft' && dx === 0) {
            dx = -1;
            dy = 0;
        } else if (event.key === 'ArrowRight' && dx === 0) {
            dx = 1;
            dy = 0;
        }
    }
});
resetGame();
isPlaying = true;
var gameSpeed = 75;

function main() {
    setTimeout(function onTick() {
        update();
        draw();
        if (!checkCollision()) {
            main();
        } else {
            resetGame();
            main();
        }
    }, gameSpeed);
}

main();