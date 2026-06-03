import os

html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Para Mi Amorcito Sara ❤️</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #ffcdd2; 
            --border-color: #4a148c; 
            --text-color: #b71c1c; 
        } 

        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: var(--bg-color);
            background-image: radial-gradient(#ffffff 15%, transparent 16%), radial-gradient(#ffffff 15%, transparent 16%);
            background-size: 60px 60px;
            background-position: 0 0, 30px 30px;
            margin: 0;
            overflow: hidden;
            font-family: 'Playfair Display', serif;
        }

        .gif {
            position: absolute;
            width: 140px; 
            height: 140px;
            object-fit: cover;
            z-index: 1;
            opacity: 0;
            transform: scale(0.5);
            border-radius: 30px;
            border: 4px solid #fff;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            transition: opacity 1.5s ease, transform 1.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        #gif1 { left: 40px; top: 40px; }      
        #gif2 { right: 40px; top: 40px; }     
        #gif3 { left: 40px; bottom: 40px; }   
        #gif4 { right: 40px; bottom: 40px; }  

        .gif.active {
            opacity: 1;
            transform: scale(1);
        }

        .container {
            position: relative;
            width: 800px;
            height: 800px;
            cursor: pointer;
            z-index: 10;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        canvas {
            position: absolute;
            z-index: 10;
            width: 800px;
            height: 800px;
        }

        #paper {
            position: absolute;
            top: 250px; 
            left: 50%;
            transform: translate(-50%, 0);
            width: 450px; 
            height: 290px; 
            background: linear-gradient(rgba(255,255,255,0.95), rgba(255,248,248,0.98)),
                        repeating-linear-gradient(transparent, transparent 21px, #fce4ec 22px);
            border: 5px double var(--border-color); 
            border-radius: 12px;
            display: flex;
            flex-direction: column; 
            justify-content: center;
            align-items: stretch; 
            padding: 20px 30px;
            box-sizing: border-box;
            z-index: 5;
            transition: transform 0.9s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.5s;
            opacity: 0;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            overflow: hidden; 
        }

        #paper p {
            color: var(--text-color);
            font-size: 0.82rem; 
            line-height: 1.45;
            text-align: justify; 
            text-justify: inter-word;
            letter-spacing: 0.2px;
            margin: 0 0 6px 0; 
            font-weight: 500;
        }

        #paper p.firma {
            text-align: center; 
            font-style: italic;
            font-weight: 700;
            font-size: 0.88rem;
            margin: 6px 0 0 0; 
            color: #d81b60;
            line-height: 1.3;
        }

        .open #paper {
            transform: translate(-50%, -260px); 
            opacity: 1;
            z-index: 20;
        }

        #start-msg {
            position: absolute;
            top: 40px;
            color: #b71c1c;
            font-weight: bold;
            font-size: 1.4rem;
            z-index: 100;
            animation: pulse 1.5s infinite;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
        }

        @keyframes pulse {
            0%, 100% { opacity: 0.6; transform: scale(1); }
            50% { opacity: 1; transform: scale(1.03); }
        }
    </style>
</head>
<body>

<div id="start-msg">Haz clic para abrir la sorpresa ❤️</div>

<audio id="musica" loop>
    <source src="musica.mp3" type="audio/mpeg">
</audio>

<img id="gif1" class="gif" src="gif1.gif">
<img id="gif2" class="gif" src="gif2.gif">
<img id="gif3" class="gif" src="gif3.gif">
<img id="gif4" class="gif" src="gif4.gif">

<div class="container" id="mainContainer" onclick="handleInteraction()">
    <div id="paper">
        <p>Aunque apenas es el comienzo de nuestra historia, cada día a tu lado me confirma lo afortunado que soy de tenerte. Gracias por tus sonrisas, por tu ternura y por hacer que este primer mes sea el más bonito de todos.</p>
        <p>¡Eres mi persona favorita, Sara! Estoy emocionado por todo lo que nos falta por vivir, descubrir y construir juntos. Te amo con todo mi corazón, hoy y muchos meses más. ❤️✨</p>
        <p class="firma">Att: Tu amorcito que será para toda la vida,<br>Yandry Figueroa ❤️</p>
    </div>
    <canvas id="canvas"></canvas>
</div>

<script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const container = document.getElementById('mainContainer');
    const audio = document.getElementById('musica');
    const startMsg = document.getElementById('start-msg');
    const gifs = [
        document.getElementById('gif1'),
        document.getElementById('gif2'),
        document.getElementById('gif3'),
        document.getElementById('gif4')
    ];
    
    let isFinished = false;
    let hasStarted = false;

    const scale = window.devicePixelRatio || 2;
    canvas.width = 800 * scale;
    canvas.height = 800 * scale;
    ctx.scale(scale, scale);

    ctx.lineWidth = 10; 
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.strokeStyle = '#000';

    async function drawRoundedRect(x, y, width, height, radius, duration = 1500) {
        return new Promise(resolve => {
            const start = performance.now();
            function animate(time) {
                let progress = (time - start) / duration;
                if (progress > 1) progress = 1;
                ctx.clearRect(0, 0, 800, 800); 
                ctx.beginPath();
                ctx.roundRect(x, y, width, height, radius);
                const length = (width * 2) + (height * 2);
                ctx.setLineDash([length, length]);
                ctx.lineDashOffset = length * (1 - progress);
                ctx.stroke();
                if (progress < 1) requestAnimationFrame(animate);
                else {
                    ctx.setLineDash([]);
                    ctx.fillStyle = '#40E0D0';
                    ctx.fill();
                    ctx.stroke();
                    resolve();
                }
            }
            requestAnimationFrame(animate);
        });
    }

    async function drawStroke(points, duration = 600) {
        return new Promise(resolve => {
            const start = performance.now();
            function animate(time) {
                let progress = (time - start) / duration;
                if (progress > 1) progress = 1;
                ctx.beginPath();
                ctx.moveTo(points[0].x, points[0].y);
                for (let i = 1; i < points.length; i++) {
                    const p1 = points[i-1];
                    const p2 = points[i];
                    const cp = (progress * (points.length - 1)) - (i - 1);
                    if (cp > 0) {
                        ctx.lineTo(p1.x + (p2.x - p1.x) * Math.min(cp, 1), 
                                   p1.y + (p2.y - p1.y) * Math.min(cp, 1));
                    }
                }
                ctx.stroke();
                if (progress < 1) requestAnimationFrame(animate);
                else resolve();
            }
            requestAnimationFrame(animate);
        });
    }

    async function drawArc(x, y, radiusX, radiusY, startAngle, endAngle, isFilled, color, duration = 400) {
        return new Promise(resolve => {
            const start = performance.now();
            function animate(time) {
                let progress = (time - start) / duration;
                if (progress > 1) progress = 1;
                ctx.beginPath();
                ctx.ellipse(x, y, radiusX, radiusY, 0, startAngle, startAngle + (endAngle - startAngle) * progress);
                if (isFilled && progress >= 1) {
                    ctx.fillStyle = color;
                    ctx.fill();
                }
                ctx.stroke();
                if (progress < 1) requestAnimationFrame(animate);
                else resolve();
            }
            requestAnimationFrame(animate);
        });
    }

    async function drawHeart(x, y, size, color = '#FF5E7E', rotation = 0, duration = 800) {
        return new Promise(resolve => {
            const start = performance.now();
            function animate(time) {
                let progress = (time - start) / duration;
                if (progress > 1) progress = 1;
                ctx.save();
                ctx.translate(x, y);
                ctx.rotate(rotation * Math.PI / 180); 
                ctx.beginPath();
                for (let t = 0; t <= progress * Math.PI * 2; t += 0.05) {
                    const dx = 16 * Math.pow(Math.sin(t), 3);
                    const dy = -(13 * Math.cos(t) - 5 * Math.cos(2*t) - 2 * Math.cos(3*t) - Math.cos(4*t));
                    const s = size / 20;
                    if (t === 0) ctx.moveTo(dx * s, dy * s);
                    else ctx.lineTo(dx * s, dy * s);
                }
                ctx.stroke();
                if (progress >= 1) { ctx.fillStyle = color; ctx.fill(); ctx.stroke(); }
                ctx.restore();
                if (progress < 1) requestAnimationFrame(animate);
                else resolve();
            }
            requestAnimationFrame(animate);
        });
    }

    async function startAnimation() {
        startMsg.style.display = 'none';
        gifs.forEach(gif => gif.classList.add('active'));

        // 1. Contorno (SOBRE GIGANTE CENTRADO)
        await drawRoundedRect(150, 250, 500, 320, 40, 1500);

        // 2. Solapa interna (V central ajustada al tamaño)
        await drawStroke([{x: 230, y: 250}, {x: 400, y: 380}], 500);
        await drawStroke([{x: 400, y: 380}, {x: 570, y: 250}], 500);

        // 3. Cara (Reubicada y más grande)
        await drawArc(330, 480, 10, 18, 0, Math.PI * 2, true, '#000');
        await drawArc(470, 480, 10, 18, 0, Math.PI * 2, true, '#000');
        await drawArc(400, 500, 15, 10, 0.2, Math.PI - 0.2, false, '#000');
        
        ctx.globalAlpha = 0.5;
        await drawArc(250, 500, 35, 20, 0, Math.PI * 2, true, '#FF99CC');
        await drawArc(550, 500, 35, 20, 0, Math.PI * 2, true, '#FF99CC');
        ctx.globalAlpha = 1;

        // 4. Sello Corazón central (MÁS GRANDE)
        await drawHeart(400, 380, 50, '#FF5E7E', 0, 800);

        // 5. Corazones periféricos (GIGANTES)
        await Promise.all([
            drawHeart(100, 150, 55, '#d81b60', -20, 700),
            drawHeart(700, 150, 45, '#d81b60', 15, 700),
            drawHeart(120, 650, 65, '#d81b60', 10, 700),
            drawHeart(680, 650, 60, '#d81b60', -15, 700)
        ]);
        
        isFinished = true;
    }

    function handleInteraction() {
        if (!hasStarted) {
            hasStarted = true;
            audio.play().catch(e => console.log("Audio play failed"));
            startAnimation();
        } else if (isFinished) {
            container.classList.toggle('open');
            canvas.style.zIndex = container.classList.contains('open') ? "1" : "10";
        }
    }
</script>

</body>
</html>
"""

# Nombre del archivo actualizado con el nombre de Sara
file_path = "carta.html"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"¡Todo listo, Yandry! El archivo ahora se guarda como '{file_path}' y el nombre ha sido cambiado por completo.")
os.startfile(file_path)