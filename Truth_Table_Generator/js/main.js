function convertExpression() {
    var expression = document.getElementById("expression").value;
    
    // Generate table headers
    var table = document.getElementById("truthTable");
    table.innerHTML = "";

    const dialog = document.getElementById("expressionsBox");
    const copybtn = document.getElementById("copy");
    const posgen = document.getElementById("possop");
    const btns = document.getElementById("btns");
    // Validate the expression
    if (expression === "") {
        btns.style.display = "none";
        copybtn.style.opacity = "0";
        posgen.style.opacity = "0";
        dialog.style.display = "none";
        table.innerHTML = "";
        return;
    }else{
        btns.style.display = "flex";
        copybtn.style.opacity = "1";
        possop.style.opacity ="1";
    }

    // Replace user-defined operations with JavaScript logical operators
    expression = expression.replace(/and/g, "&&");
    expression = expression.replace(/or/g, "||");
    expression = expression.replace(/\*+/g, "&&");
    expression = expression.replace(/\++/g, "||");

    // Find unique variables used in the expression
    var variables = expression.match(/[a-zA-Z]+/g);
    variables = Array.from(new Set(variables));

    

    var tableHeader = table.createTHead();
    var headerRow = tableHeader.insertRow();

    // Add variables as header cells
    for (var i = 0; i < variables.length; i++) {
        var headerCell = document.createElement("th");
        headerCell.innerHTML = variables[i];
        headerRow.appendChild(headerCell);
    }

    // Add expression as header cell
    var expressionHeader = document.createElement("th");
    expressionHeader.innerHTML = `F`;
    headerRow.appendChild(expressionHeader);

    // Add minterms and maxterms as header cells
    var mintermsHeader = document.createElement("th");
    mintermsHeader.innerHTML = "Minterms";
    headerRow.appendChild(mintermsHeader);

    var maxtermsHeader = document.createElement("th");
    maxtermsHeader.innerHTML = "Maxterms";
    headerRow.appendChild(maxtermsHeader);

    // Generate truth table rows
    var rowCount = Math.pow(2, variables.length);
    for (var i = 0; i < rowCount; i++) {
        var row = table.insertRow();

        // Add variable values as cells
        for (var j = variables.length - 1; j >= 0; j--) {
            var cell = row.insertCell();
            var value = (i >> j) & 1;
            cell.innerHTML = value;
        }

        // Add expression result as cell
        var result = evaluateExpression(expression, variables, i);
        var resultCell = row.insertCell();
        resultCell.innerHTML = result;

        // Add minterms and maxterms as cells
        var mintermsCell = row.insertCell();
        mintermsCell.innerHTML = getMinterms(expression, variables, i);

        var maxtermsCell = row.insertCell();
        maxtermsCell.innerHTML = getMaxterms(expression, variables, i);
    }       
}

function evaluateExpression(expression, variables, row) {
    for (var i = 0; i < variables.length; i++) {
        expression = expression.replace(new RegExp(variables[i], 'g'), ((row >> (variables.length - i - 1)) & 1));
    }

    return +eval(expression);
}

function getMinterms(expression, variables, row) {
    var minterms = [];

    for (var i = 0; i < variables.length; i++) {
        expression = expression.replace(new RegExp(variables[i], 'g'), (row >> (variables.length - i - 1)) % 2);
    }

    if (evaluateExpression(expression, variables, row)) {
        var minterm = "";
        for (var i = 0; i < variables.length; i++) {
            if ((row >> (variables.length - i - 1)) % 2 === 1) {
                minterm += variables[i];
            } else {
                minterm +=  variables[i] + "'";
            }
        }
        minterms.push(minterm);
    }

    return minterms.join(", ");
}

function getMaxterms(expression, variables, row) {
    var maxterms = [];

    for (var i = 0; i < variables.length; i++) {
        expression = expression.replace(new RegExp(variables[i], 'g'), (row >> (variables.length - i - 1)) % 2);
    }

    if (!evaluateExpression(expression, variables, row)) {
        var maxterm = "";
        for (var i = 0; i < variables.length; i++) {
            if ((row >> (variables.length - i - 1)) % 2 === 0) {
                maxterm += variables[i];
            } else {
                maxterm +=  variables[i] + "'" ;
            }
            if(i !== variables.length-1){
                maxterm += "+"    
            }
        }
        maxterms.push(maxterm);
    }

    return maxterms.join(", ");
}

// copy table function
function copyTable() {
  // Get the table element
  var table = document.getElementById("truthTable");

  // Create a range object to select the table content
  var range = document.createRange();
  range.selectNode(table);

  // Add the range to the user's selection
  var selection = window.getSelection();
  selection.removeAllRanges();
  selection.addRange(range);

  // Copy the selected content to the clipboard
  document.execCommand("copy");

  // Clear the selection
  selection.removeAllRanges();
  const msg = document.getElementById("msg");
  msg.style.right = "20px";
  // Format the copied content
  var copiedContent = table.innerHTML
    .replace(/<tr>/g, "\n") // Replace <tr> tags with line breaks
    .replace(/<\/tr>/g, "") // Remove </tr> tags
    .replace(/<th>/g, "\t\t") // Replace <th> tags with tabs
    .replace(/<\/th>/g, "") // Remove </th> tags
    .replace(/<td>/g, "\t\t") // Replace <td> tags with tabs
    .replace(/<\/td>/g, ""); // Remove </td> tags
  console.log(copiedContent);
  setTimeout(function() {
    msg.style.right = "-200px";
  }, 1000);
}

// Generate SOP and POS functions deploy
function generateExpressions() {
  // Get the table element
  var table = document.getElementById("truthTable");
  const dialog = document.getElementById("expressionsBox");
  dialog.style.display = "flex";
  // Get the minterms and maxterms from the table
  var minterms = [];
  var maxterms = [];

  // Traverse the table rows
  for (var i = 1; i < table.rows.length; i++) {
    var mintermsCell = table.rows[i].cells[table.rows[i].cells.length - 2];
    var maxtermsCell = table.rows[i].cells[table.rows[i].cells.length - 1];

    var mintermsList = mintermsCell.innerHTML.split(", ");
    var maxtermsList = maxtermsCell.innerHTML.split(", ");

    minterms = minterms.concat(mintermsList);
    maxterms = maxterms.concat(maxtermsList);
  }

  // Remove duplicate minterms and maxterms
  minterms = [...new Set(minterms)];
  maxterms = [...new Set(maxterms)];

  // Generate SOP and POS expressions
  var sopExpression = generateSOP(minterms);
  var posExpression = generatePOS(maxterms);

  // Display the expressions in the expressionsBox
  var expressionsBox = document.getElementById("expressionsBox");
  expressionsBox.innerHTML = "<p> SOP : <span>" + sopExpression + "</span></p>" + "<p> POS : <span>" + posExpression + "</span></p>";
}

function generateSOP(minterms) {
  var sopExpression = "";

  for (var i = 0; i < minterms.length; i++) {
    var term = minterms[i];
    var subExpression = "";
    if(term == ""){
        continue;
    }else{
        for (var j = 0; j < term.length; j++) {
          var variable = term[j];

          if (variable !== "'") {
            subExpression += variable;
          } else {
            subExpression += "!";
          }
        }

        sopExpression += "(" + subExpression + ")";
        if (i !== minterms.length - 1) {
          sopExpression += " + ";
        }
    }
  }

  return sopExpression;
}

function generatePOS(maxterms) {
  var posExpression = "";

  for (var i = 0; i < maxterms.length; i++) {
    var term = maxterms[i];
    if(term == ""){
        continue;
    }else{
        var subExpression = "";

        for (var j = 0; j < term.length; j++) {
          var variable = term[j];

          if (variable !== "'") {
            subExpression += variable;
          } else {
            subExpression += "!";
          }
        }

        posExpression += "(" + subExpression + ")";
        if (i !== maxterms.length - 1) {
          posExpression += " * ";
        }
    }
  }

  return posExpression;
}