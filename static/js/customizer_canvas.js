// Atelier Customizer Canvas Visualizer
let canvas, ctx;

const state = {
    shapeCode: 'pleated_lamp',
    glazeColor: '#F2EDE4',
    accentColor: '#DFD5C6',
    textureType: 'speckled',
    standColor: 'white',
    engravingText: '',
    lightGlow: true
};

function initCustomizerCanvas() {
    canvas = document.getElementById('atelier-canvas');
    if (!canvas) return;
    ctx = canvas.getContext('2d');
    renderCeramicPiece();
}

function hexToRgb(hex) {
    hex = hex.replace(/^#/, '');
    if (hex.length === 3) {
        hex = hex.split('').map(c => c + c).join('');
    }
    const num = parseInt(hex, 16);
    return {
        r: (num >> 16) & 255,
        g: (num >> 8) & 255,
        b: num & 255
    };
}

function renderCeramicPiece() {
    if (!ctx || !canvas) return;
    const w = canvas.width;
    const h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    const rgb = hexToRgb(state.glazeColor);
    const accRgb = hexToRgb(state.accentColor);

    // 1. Studio Backdrop & Oak Tabletop
    const bgGrad = ctx.createLinearGradient(0, 0, 0, h);
    bgGrad.addColorStop(0, '#FAF7F2');
    bgGrad.addColorStop(0.7, '#F2EBE1');
    bgGrad.addColorStop(1, '#E5DCCE');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, w, h);

    // Tabletop line
    const tableY = h * 0.76;
    const tableGrad = ctx.createLinearGradient(0, tableY, 0, h);
    tableGrad.addColorStop(0, '#DFD1BF');
    tableGrad.addColorStop(0.08, '#D1C0AB');
    tableGrad.addColorStop(1, '#BFA992');
    ctx.fillStyle = tableGrad;
    ctx.fillRect(0, tableY, w, h - tableY);

    // Table edge highlight & shadow
    ctx.strokeStyle = '#FFFFFF';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(0, tableY);
    ctx.lineTo(w, tableY);
    ctx.stroke();

    const cx = w / 2;
    const cy = h * 0.48;

    // 2. Base Drop Shadow
    ctx.save();
    ctx.beginPath();
    ctx.ellipse(cx, tableY + 8, w * 0.28, 14, 0, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(70, 50, 35, 0.22)';
    ctx.filter = 'blur(10px)';
    ctx.fill();
    ctx.restore();

    // 3. Render Specific Shape
    if (state.shapeCode === 'pleated_lamp') {
        renderPleatedLamp(cx, cy, rgb, accRgb, tableY);
    } else if (state.shapeCode === 'fluted_vase') {
        renderFlutedVase(cx, cy, rgb, accRgb, tableY);
    } else if (state.shapeCode === 'donut_flask') {
        renderDonutFlask(cx, cy, rgb, accRgb, tableY);
    } else if (state.shapeCode === 'desk_cup') {
        renderDeskCup(cx, cy, rgb, accRgb, tableY);
    } else if (state.shapeCode === 'tea_bowl') {
        renderTeaBowl(cx, cy, rgb, accRgb, tableY);
    }

    // 4. Custom Artisan Monogram Stamp
    if (state.engravingText) {
        renderEngravingStamp(cx, tableY - 14);
    }

    // Update hidden input with canvas snapshot
    const previewInput = document.getElementById('preview_data_url');
    if (previewInput) {
        previewInput.value = canvas.toDataURL('image/jpeg', 0.85);
    }
}

function renderPleatedLamp(cx, cy, rgb, accRgb, tableY) {
    const lampCenterY = cy - 20;

    // Ambient Warm Light Glow
    if (state.lightGlow) {
        const glow = ctx.createRadialGradient(cx, lampCenterY + 40, 20, cx, lampCenterY + 40, 260);
        glow.addColorStop(0, 'rgba(255, 230, 160, 0.65)');
        glow.addColorStop(0.35, 'rgba(255, 215, 120, 0.35)');
        glow.addColorStop(0.7, 'rgba(240, 185, 90, 0.12)');
        glow.addColorStop(1, 'rgba(240, 185, 90, 0)');
        ctx.fillStyle = glow;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    // Architectural Wire Tripod Stand
    let standStroke = '#FFFFFF';
    if (state.standColor === 'brass') standStroke = '#C8A362';
    if (state.standColor === 'matte_black') standStroke = '#2D2926';

    const collarY = lampCenterY + 115;
    const footY = tableY - 5;
    const footLeftX = cx - 110;
    const footRightX = cx + 110;
    const footBackX = cx;

    ctx.strokeStyle = standStroke;
    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    // Back leg
    ctx.beginPath();
    ctx.moveTo(cx, collarY);
    ctx.lineTo(footBackX, footY - 35);
    ctx.stroke();

    // Left trapezoid wire leg
    ctx.beginPath();
    ctx.moveTo(cx - 15, collarY);
    ctx.lineTo(footLeftX, footY);
    ctx.lineTo(footLeftX + 35, footY);
    ctx.lineTo(cx - 5, collarY + 20);
    ctx.stroke();

    // Right trapezoid wire leg
    ctx.beginPath();
    ctx.moveTo(cx + 15, collarY);
    ctx.lineTo(footRightX, footY);
    ctx.lineTo(footRightX - 35, footY);
    ctx.lineTo(cx + 5, collarY + 20);
    ctx.stroke();

    // Braided power cord dropping down
    ctx.strokeStyle = 'rgba(200, 190, 175, 0.9)';
    ctx.lineWidth = 3.5;
    ctx.beginPath();
    ctx.moveTo(cx, collarY + 10);
    ctx.bezierCurveTo(cx - 10, collarY + 80, cx + 15, footY - 20, cx - 25, footY);
    ctx.stroke();

    // Ceramic Collar / Socket Holder
    ctx.fillStyle = `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`;
    ctx.beginPath();
    ctx.roundRect(cx - 24, collarY - 10, 48, 26, 6);
    ctx.fill();
    ctx.strokeStyle = `rgb(${accRgb.r}, ${accRgb.g}, ${accRgb.b})`;
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Hand-Pleated Conical Shade
    const topRadius = 38;
    const bottomRadius = 165;
    const shadeTopY = lampCenterY - 145;
    const shadeBottomY = lampCenterY + 105;
    const pleatCount = 28;

    // Draw pleat folds
    for (let i = 0; i < pleatCount; i++) {
        const t1 = (i / pleatCount) * Math.PI;
        const t2 = ((i + 1) / pleatCount) * Math.PI;

        const xTop1 = cx + Math.cos(t1 - Math.PI) * topRadius;
        const xTop2 = cx + Math.cos(t2 - Math.PI) * topRadius;
        const xBot1 = cx + Math.cos(t1 - Math.PI) * bottomRadius;
        const xBot2 = cx + Math.cos(t2 - Math.PI) * bottomRadius;

        ctx.beginPath();
        ctx.moveTo(xTop1, shadeTopY);
        ctx.lineTo(xTop2, shadeTopY);
        ctx.lineTo(xBot2, shadeBottomY);
        ctx.lineTo(xBot1, shadeBottomY);
        ctx.closePath();

        // Alternating pleat shadow and illumination
        const shadeFactor = (i % 2 === 0) ? 0.92 : 1.08;
        const rVal = Math.min(255, Math.floor(rgb.r * shadeFactor * 1.15));
        const gVal = Math.min(255, Math.floor(rgb.g * shadeFactor * 1.12));
        const bVal = Math.min(255, Math.floor(rgb.b * shadeFactor * 1.05));

        ctx.fillStyle = `rgb(${rVal}, ${gVal}, ${bVal})`;
        ctx.fill();

        ctx.strokeStyle = 'rgba(150, 130, 110, 0.25)';
        ctx.lineWidth = 0.8;
        ctx.stroke();
    }

    // Top scalloped/serrated ring
    ctx.beginPath();
    ctx.ellipse(cx, shadeTopY, topRadius, 9, 0, 0, Math.PI * 2);
    ctx.fillStyle = `rgb(${accRgb.r}, ${accRgb.g}, ${accRgb.b})`;
    ctx.fill();

    // Bottom soft shade edge
    ctx.beginPath();
    ctx.ellipse(cx, shadeBottomY, bottomRadius, 18, 0, 0, Math.PI);
    ctx.strokeStyle = 'rgba(120, 100, 80, 0.2)';
    ctx.lineWidth = 2;
    ctx.stroke();

    applyGlazeTexture(cx - bottomRadius, shadeTopY, bottomRadius * 2, shadeBottomY - shadeTopY);
}

function renderFlutedVase(cx, cy, rgb, accRgb, tableY) {
    const vaseW = 150;
    const vaseH = 340;
    const topY = cy - 160;
    const baseWidth = 85;

    ctx.save();
    ctx.beginPath();
    ctx.moveTo(cx - 32, topY);
    ctx.quadraticCurveTo(cx - 36, topY + 60, cx - vaseW, topY + 160);
    ctx.quadraticCurveTo(cx - vaseW * 0.8, topY + 260, cx - baseWidth, tableY);
    ctx.lineTo(cx + baseWidth, tableY);
    ctx.quadraticCurveTo(cx + vaseW * 0.8, topY + 260, cx + vaseW, topY + 160);
    ctx.quadraticCurveTo(cx + 36, topY + 60, cx + 32, topY);
    ctx.closePath();

    // Ceramic gradient
    const grad = ctx.createLinearGradient(cx - vaseW, 0, cx + vaseW, 0);
    grad.addColorStop(0, `rgb(${Math.max(0, rgb.r - 40)}, ${Math.max(0, rgb.g - 40)}, ${Math.max(0, rgb.b - 40)})`);
    grad.addColorStop(0.3, `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`);
    grad.addColorStop(0.65, `rgb(${Math.min(255, rgb.r + 25)}, ${Math.min(255, rgb.g + 25)}, ${Math.min(255, rgb.b + 25)})`);
    grad.addColorStop(1, `rgb(${Math.max(0, rgb.r - 45)}, ${Math.max(0, rgb.g - 45)}, ${Math.max(0, rgb.b - 45)})`);
    ctx.fillStyle = grad;
    ctx.fill();

    // Carved fluting ridges
    ctx.strokeStyle = `rgba(${accRgb.r - 20}, ${accRgb.g - 20}, ${accRgb.b - 20}, 0.55)`;
    ctx.lineWidth = 3.5;
    for (let ox = -vaseW + 30; ox <= vaseW - 30; ox += 28) {
        ctx.beginPath();
        ctx.moveTo(cx + ox * 0.25, topY + 70);
        ctx.quadraticCurveTo(cx + ox * 0.9, topY + 180, cx + (ox / vaseW) * baseWidth, tableY);
        ctx.stroke();
    }

    // Flared Lip rim
    ctx.beginPath();
    ctx.ellipse(cx, topY, 34, 11, 0, 0, Math.PI * 2);
    ctx.fillStyle = `rgb(${accRgb.r}, ${accRgb.g}, ${accRgb.b})`;
    ctx.fill();
    ctx.stroke();

    ctx.restore();
    applyGlazeTexture(cx - vaseW, topY, vaseW * 2, vaseH);
}

function renderDonutFlask(cx, cy, rgb, accRgb, tableY) {
    const outerR = 145;
    const innerR = 60;
    const neckTopY = cy - outerR - 45;

    ctx.save();
    // Neck
    ctx.fillStyle = `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`;
    ctx.fillRect(cx - 25, neckTopY, 50, 55);
    ctx.beginPath();
    ctx.ellipse(cx, neckTopY, 25, 8, 0, 0, Math.PI * 2);
    ctx.fillStyle = `rgb(${accRgb.r}, ${accRgb.g}, ${accRgb.b})`;
    ctx.fill();

    // Donut Body
    ctx.beginPath();
    ctx.arc(cx, cy + 10, outerR, 0, Math.PI * 2);
    ctx.arc(cx, cy + 10, innerR, 0, Math.PI * 2, true);
    
    const donutGrad = ctx.createRadialGradient(cx - 30, cy - 20, 20, cx, cy, outerR);
    donutGrad.addColorStop(0, `rgb(${Math.min(255, rgb.r + 30)}, ${Math.min(255, rgb.g + 30)}, ${Math.min(255, rgb.b + 30)})`);
    donutGrad.addColorStop(0.7, `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`);
    donutGrad.addColorStop(1, `rgb(${Math.max(0, rgb.r - 40)}, ${Math.max(0, rgb.g - 40)}, ${Math.max(0, rgb.b - 40)})`);
    ctx.fillStyle = donutGrad;
    ctx.fill();

    ctx.restore();
    applyGlazeTexture(cx - outerR, cy - outerR, outerR * 2, outerR * 2);
}

function renderDeskCup(cx, cy, rgb, accRgb, tableY) {
    const cupW = 85;
    const cupH = 175;
    const topY = tableY - cupH;

    // Writing pencils inside cup (from photo)
    const pencils = [
        { color: '#2B2621', angle: -0.22, height: 95 },
        { color: '#C4704F', angle: -0.08, height: 115 },
        { color: '#D9A74A', angle: 0.12, height: 105 },
        { color: '#EAE3D7', angle: 0.25, height: 90 },
    ];

    pencils.forEach(p => {
        ctx.save();
        ctx.translate(cx + (p.angle * 60), topY + 10);
        ctx.rotate(p.angle);
        ctx.fillStyle = p.color;
        ctx.fillRect(-6, -p.height, 12, p.height);
        // Sharpened wood tip
        ctx.beginPath();
        ctx.moveTo(-6, -p.height);
        ctx.lineTo(6, -p.height);
        ctx.lineTo(0, -p.height - 20);
        ctx.fillStyle = '#E5C79E';
        ctx.fill();
        // Graphite tip
        ctx.beginPath();
        ctx.moveTo(-2, -p.height - 14);
        ctx.lineTo(2, -p.height - 14);
        ctx.lineTo(0, -p.height - 20);
        ctx.fillStyle = '#222';
        ctx.fill();
        ctx.restore();
    });

    // Cup Body
    const cupGrad = ctx.createLinearGradient(cx - cupW, 0, cx + cupW, 0);
    cupGrad.addColorStop(0, `rgb(${Math.max(0, rgb.r - 35)}, ${Math.max(0, rgb.g - 35)}, ${Math.max(0, rgb.b - 35)})`);
    cupGrad.addColorStop(0.3, `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`);
    cupGrad.addColorStop(0.7, `rgb(${Math.min(255, rgb.r + 20)}, ${Math.min(255, rgb.g + 20)}, ${Math.min(255, rgb.b + 20)})`);
    cupGrad.addColorStop(1, `rgb(${Math.max(0, rgb.r - 40)}, ${Math.max(0, rgb.g - 40)}, ${Math.max(0, rgb.b - 40)})`);

    ctx.fillStyle = cupGrad;
    ctx.fillRect(cx - cupW, topY, cupW * 2, cupH);

    // Rim & base ellipses
    ctx.beginPath();
    ctx.ellipse(cx, topY, cupW, 16, 0, 0, Math.PI * 2);
    ctx.fillStyle = `rgb(${accRgb.r}, ${accRgb.g}, ${accRgb.b})`;
    ctx.fill();

    ctx.beginPath();
    ctx.ellipse(cx, tableY, cupW, 16, 0, 0, Math.PI);
    ctx.fillStyle = `rgb(${Math.max(0, rgb.r - 30)}, ${Math.max(0, rgb.g - 30)}, ${Math.max(0, rgb.b - 30)})`;
    ctx.fill();

    applyGlazeTexture(cx - cupW, topY, cupW * 2, cupH);
}

function renderTeaBowl(cx, cy, rgb, accRgb, tableY) {
    const bowlR = 140;
    const bowlTopY = tableY - 130;

    ctx.save();
    // Bowl body
    ctx.beginPath();
    ctx.arc(cx, bowlTopY + 15, bowlR, 0, Math.PI);
    ctx.lineTo(cx - bowlR * 0.45, tableY);
    ctx.lineTo(cx + bowlR * 0.45, tableY);
    ctx.closePath();

    const bowlGrad = ctx.createLinearGradient(cx - bowlR, 0, cx + bowlR, 0);
    bowlGrad.addColorStop(0, `rgb(${Math.max(0, rgb.r - 40)}, ${Math.max(0, rgb.g - 40)}, ${Math.max(0, rgb.b - 40)})`);
    bowlGrad.addColorStop(0.35, `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`);
    bowlGrad.addColorStop(0.8, `rgb(${Math.min(255, rgb.r + 20)}, ${Math.min(255, rgb.g + 20)}, ${Math.min(255, rgb.b + 20)})`);
    bowlGrad.addColorStop(1, `rgb(${Math.max(0, rgb.r - 35)}, ${Math.max(0, rgb.g - 35)}, ${Math.max(0, rgb.b - 35)})`);
    ctx.fillStyle = bowlGrad;
    ctx.fill();

    // Wabi-sabi top lip
    ctx.beginPath();
    ctx.ellipse(cx, bowlTopY + 15, bowlR, 35, 0, 0, Math.PI * 2);
    ctx.fillStyle = `rgb(${accRgb.r}, ${accRgb.g}, ${accRgb.b})`;
    ctx.fill();
    ctx.strokeStyle = `rgba(80, 60, 40, 0.3)`;
    ctx.lineWidth = 1.5;
    ctx.stroke();

    ctx.restore();
    applyGlazeTexture(cx - bowlR, bowlTopY, bowlR * 2, 130);
}

function applyGlazeTexture(x, y, w, h) {
    if (state.textureType === 'speckled') {
        ctx.fillStyle = 'rgba(60, 50, 40, 0.35)';
        for (let i = 0; i < 280; i++) {
            const sx = x + Math.random() * w;
            const sy = y + Math.random() * h;
            const size = Math.random() * 2.2 + 0.6;
            ctx.beginPath();
            ctx.arc(sx, sy, size, 0, Math.PI * 2);
            ctx.fill();
        }
    } else if (state.textureType === 'crackle_celadon') {
        ctx.strokeStyle = 'rgba(60, 80, 60, 0.25)';
        ctx.lineWidth = 1.2;
        for (let i = 0; i < 18; i++) {
            const startX = x + Math.random() * w;
            const startY = y + Math.random() * h;
            ctx.beginPath();
            ctx.moveTo(startX, startY);
            ctx.lineTo(startX + (Math.random() - 0.5) * 60, startY + Math.random() * 40);
            ctx.lineTo(startX + (Math.random() - 0.5) * 80, startY + Math.random() * 80);
            ctx.stroke();
        }
    }
}

function renderEngravingStamp(cx, cy) {
    ctx.save();
    ctx.beginPath();
    ctx.arc(cx, cy, 26, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(235, 225, 210, 0.85)';
    ctx.fill();
    ctx.strokeStyle = 'rgba(140, 100, 70, 0.7)';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    ctx.fillStyle = '#4A3B32';
    ctx.font = 'bold 11px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(state.engravingText.toUpperCase(), cx, cy);
    ctx.restore();
}

window.updateAtelierShape = function(shapeCode, shapeName, basePrice) {
    state.shapeCode = shapeCode;
    const standGroup = document.getElementById('stand-color-group');
    if (standGroup) {
        standGroup.style.display = (shapeCode === 'pleated_lamp') ? 'block' : 'none';
    }
    renderCeramicPiece();
    updateLivePrice();
};

window.updateAtelierGlaze = function(hex, accent, texture, glazeName, modifier) {
    state.glazeColor = hex;
    state.accentColor = accent;
    state.textureType = texture;
    renderCeramicPiece();
    updateLivePrice();
};

window.updateAtelierStand = function(standColor) {
    state.standColor = standColor;
    renderCeramicPiece();
};

window.updateAtelierEngraving = function(text) {
    state.engravingText = text.trim().slice(0, 15);
    renderCeramicPiece();
    updateLivePrice();
};

window.toggleAtelierGlow = function() {
    state.lightGlow = !state.lightGlow;
    renderCeramicPiece();
};

function updateLivePrice() {
    const shapeEl = document.querySelector('input[name="shape_id"]:checked');
    const glazeEl = document.querySelector('input[name="glaze_id"]:checked');
    const engravingEl = document.getElementById('engraving-input');
    const priceDisplay = document.getElementById('atelier-live-price');

    if (!shapeEl || !glazeEl || !priceDisplay) return;

    const basePrice = parseFloat(shapeEl.dataset.price || '0');
    const glazeModifier = parseFloat(glazeEl.dataset.modifier || '0');
    const engravingFee = (engravingEl && engravingEl.value.trim().length > 0) ? 8.00 : 0.00;

    const total = basePrice + glazeModifier + engravingFee;
    priceDisplay.textContent = `$${total.toFixed(2)}`;
}

document.addEventListener('DOMContentLoaded', initCustomizerCanvas);
