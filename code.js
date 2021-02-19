function functionA() {
	a = document.getElementById("circle#kota");

	if (a != null)
		a.style.fill = 'yellow';
}

function onChangeHeight() {
	a = document.getElementById("stupidId");

	if (a != null)
		a.setAttributeNS(null, "height", 200);
}

function drawGrid(root) {
	var i;
	var j;
	var xmlns = "http://www.w3.org/2000/svg";
	for (i = 0; i < 10; i++) {
		var h = document.createElementNS(xmlns, "line");
		h.setAttributeNS(null, "id", "line_H_".concat(i.toString()));
		h.setAttributeNS(null, "x1", 0);
		h.setAttributeNS(null, "y1", i * 30);
		h.setAttributeNS(null, "x2", 270);
		h.setAttributeNS(null, "y2", i * 30);

		var v = document.createElementNS(xmlns, "line");
		v.setAttributeNS(null, "id", "line_V_".concat(i.toString()));
		v.setAttributeNS(null, "y1", 0);
		v.setAttributeNS(null, "x1", i * 30);
		v.setAttributeNS(null, "y2", 270);
		v.setAttributeNS(null, "x2", i * 30);

		root.appendChild(h);
		root.appendChild(v);
		if (i != 9)
			for (j = 0; j < 9; j++) {

				var S = document.createElementNS(xmlns, "text");
				S.setAttribute('x', i * 30);
				S.setAttribute('y', j * 30 + 20);
				S.textContent = 'IJ'.concat(i.toString(), j.toString());

				root.appendChild(S);

			}
	}
}

function onLoad() {
	var xmlns = "http://www.w3.org/2000/svg";
	var boxWidth = 300;
	var boxHeight = 300;

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