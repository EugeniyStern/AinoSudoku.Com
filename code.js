function onChangeHeight() {
	a = document.getElementById("stupidId");

	var i = 5;
	var j = 6;
	var id = 'IJ'.concat(i.toString(), j.toString());
	a = document.getElementById(id);
	a.textContent = '6';
}

function drawGrid(root) {

	var active_i = 0;
	var active_j = 0;
	var active_f = 0;

	root.addEventListener('mousedown', startDrag);
	root.addEventListener('mousemove', drag);
	root.addEventListener('mouseup', endDrag);
	root.addEventListener('mouseleave', endDrag);

	function mouseOver(evt) {
		evt.target.setAttributeNS(null, "fill-opacity", 0.3);

		id = evt.target.id;

		active_i = parseInt(id.substring(4, 5));
		active_j = parseInt(id.substring(5, 6));

	}

	function mouseOut(evt) {
		evt.target.setAttributeNS(null, "fill-opacity", 0);
	}

	function getMousePosition(evt) {
		var CTM = root.getScreenCTM();
		if (evt.touches) {
			evt = evt.touches[0];
		}
		return {
			x : (evt.clientX - CTM.e) / CTM.a,
			y : (evt.clientY - CTM.f) / CTM.d
		};
	}

	// Geometry

	const Grid_B_factor = 90;
	const Grid_A_factor = 300;
	const Grid_X_Start = 100;
	const Grid_Y_Start = 100;
	const Text_X_Shift = 30;
	const Text_Y_Shift = 60;
	const Text_Font_Size = '40px';

	var i, xa, xb, ya, yb, x, y;
	var j;
	var h;
	var v;
	var id;

	var keep_X;
	var keep_Y;

	var xmlns = "http://www.w3.org/2000/svg";

	for (xa = 0; xa < 3; xa++)
		for (xb = 0; xb < 3; xb++)
			for (ya = 0; ya < 3; ya++)
				for (yb = 0; yb < 3; yb++) {

					i = xa * 3 + xb + 1;
					j = ya * 3 + yb + 1;

					Small_Square = document.createElementNS(xmlns, "rect");
					Small_Square_Id = "S_IJ".concat(i.toString(), j.toString());
					Small_Square.setAttributeNS(null, "id", Small_Square_Id);

					// position
					x = Grid_X_Start + Grid_A_factor * xa + Grid_B_factor * xb
							+ (Grid_A_factor - 3 * Grid_B_factor) * (1 - xa)
							/ 3;
					Small_Square.setAttribute('x', x);

					y = Grid_Y_Start + Grid_A_factor * ya + Grid_B_factor * yb
							+ (Grid_A_factor - 3 * Grid_B_factor) * (1 - ya)
							/ 3;
					Small_Square.setAttribute('y', y);

					// size
					Small_Square.setAttributeNS(null, "width", Grid_B_factor);
					Small_Square.setAttributeNS(null, "height", Grid_B_factor);

					// look and fill
					Small_Square.setAttributeNS(null, "fill", "red");
					Small_Square.addEventListener('mouseover', mouseOver);
					Small_Square.addEventListener('mouseout', mouseOut);

//					Small_Square.addEventListener('touchstart', startDrag);
//					Small_Square.addEventListener('touchmove', drag);
//					 svg.addEventListener('touchend', endDrag);
//					 svg.addEventListener('touchleave', endDrag);
//					 svg.addEventListener('touchcancel', endDrag);

					root.appendChild(Small_Square);

					var S = document.createElementNS(xmlns, "text");
					S.setAttribute('x', x + Text_X_Shift);
					S.setAttribute('y', y + Text_Y_Shift);

					id = 'T_IJ'.concat(i.toString(), j.toString());
					S.textContent = '';
					S.setAttribute('id', id);
					S.setAttribute('font-size', Text_Font_Size);
					S.setAttribute('class', 'draggable')

					root.appendChild(S);
				}

	for (ya = 0; ya < 3; ya++)
		for (yb = 0; yb < 3; yb++) {
			i = ya * 3 + yb + 1;

			var S = document.createElementNS(xmlns, "text");

			// position
			x = Grid_X_Start + Grid_A_factor * 3 + Grid_B_factor;

			y = Grid_Y_Start + Grid_A_factor * ya + Grid_B_factor * yb
					+ (Grid_A_factor - 3 * Grid_B_factor) * (1 - ya) / 3;

			S.setAttribute('x', x + Text_X_Shift);
			S.setAttribute('y', y + Text_Y_Shift);

			S.textContent = i.toString();
			id = 'FIG_'.concat(i.toString());
			S.setAttribute('id', id);
			S.setAttribute('font-size', Text_Font_Size);
			S.setAttribute('class', 'draggable')

			root.appendChild(S);
		}

	var offset, transform;
	var selectedElement = false;

	function startDrag(evt) {
		if (evt.target.classList.contains('draggable')) {
			selectedElement = evt.target;
			keep_X = parseInt(selectedElement.getAttribute("x"));
			keep_Y = parseInt(selectedElement.getAttribute("y"));

			offset = getMousePosition(evt);

			// Get all the transforms currently on this element
			var transforms = selectedElement.transform.baseVal;

			// Ensure the first transform is a translate transform
			if (transforms.length === 0
					|| transforms.getItem(0).type !== SVGTransform.SVG_TRANSFORM_TRANSLATE) {
				// Create an transform that translates by (0, 0)
				var translate = root.createSVGTransform();
				translate.setTranslate(0, 0);
				// Add the translation to the front of the transforms list
				selectedElement.transform.baseVal
						.insertItemBefore(translate, 0);
			}

			// Get initial translation amount
			transform = transforms.getItem(0);
			offset.x -= transform.matrix.e;
			offset.y -= transform.matrix.f;

			if (evt.target.id.substr(0, 3) == "FIG") {
				active_f = parseInt(evt.target.id.substr(4, 1));
			}
			if (evt.target.id.substr(0, 4) == "T_IJ") {
				active_f = parseInt(evt.target.id.substr(4, 1));
			}
		}
	}
	function drag(evt) {
		if (selectedElement) {
			evt.preventDefault();
			var coord = getMousePosition(evt);
			transform.setTranslate(coord.x - offset.x, coord.y - offset.y);
		}
	}
	function endDrag(evt) {

		if ((selectedElement != null)
				&& (selectedElement.setAttribute != undefined)) {

			transform.setTranslate(0, 0);
		}

		selectedElement = null;

		var i = active_i;
		var j = active_j;

		var id = 'T_IJ'.concat(i.toString(), j.toString());
		a = document.getElementById(id);
		a.textContent = active_f.toString();
	}

}

function onLoad() {
	var xmlns = "http://www.w3.org/2000/svg";
	var boxWidth = 1300;
	var boxHeight = 1100;

	var svgElem = document.createElementNS(xmlns, "svg");
	svgElem
			.setAttributeNS(null, "viewBox", "0 0 " + boxWidth + " "
					+ boxHeight);

	svgElem.setAttributeNS(null, "width", boxWidth);
	svgElem.setAttributeNS(null, "height", boxHeight);

	svgElem.style.display = "block";

	drawGrid(svgElem);

	var svgContainer = document.getElementById("svgContainer");
	svgElem.setAttributeNS(null, "stroke", "black");
	svgContainer.appendChild(svgElem);
}
