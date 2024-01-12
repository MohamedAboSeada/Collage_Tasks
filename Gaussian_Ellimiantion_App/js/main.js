let selects = document.querySelectorAll('select');
for(let i = 1;i<=20;i++){
    selects.forEach(select => {
        let option = document.createElement('option');
        option.value = i;
        option.textContent = i;
        select.append(option);
    });
}

let generatebtn = document.querySelector('#gene');
let table = document.querySelector('#one');
function generateMatrix(row,column){
    table.innerHTML = ``;
    for(let i = 0;i<row;i++){
        let ro = document.createElement('tr');
        for(let j = 0;j<column;j++){
            let col = document.createElement('td');
            let input = document.createElement('input');
            input.type='text';
            col.append(input);
            ro.append(col)
        }
        table.append(ro)
    }
    let tableFirstInput = document.querySelector('table tr td input');
    tableFirstInput.focus();
    update();
}

generatebtn.addEventListener('click',_=>{
   generateMatrix(selects[0].value,selects[1].value);
});

function update(){
    // makeing table mechanism
    let inputs = document.querySelectorAll('table tr td input')
    inputs.forEach((input,index) => {
        input.addEventListener('input',_=>{
            if(input.value === ``){
                inputs[index-1].focus();
                inputs[index-1].select();
            } 
        });
        input.addEventListener('keydown',e=>{
            if(e.keyCode === 39 && index != inputs.length - 1){
                inputs[index+1].focus();
            }
            if(e.keyCode === 37 && index !== 0){
                inputs[index-1].focus();
            }
        });
    });
   
    let solve = document.querySelector('#solve');
    solve.addEventListener('click',_=>{
        let allinputsFilled = true;
        let inputNumbers = [];
        // check for empty cells before solve
        inputs.forEach(input => {
            inputNumbers.push(+input.value);
            if(input.value == ''){
                allinputsFilled = false;
                input.style.borderColor = `red`; 
                input.style.boxShadow = `0 0 10px rgb(255 0 0 / 20%)`; 
            }else{
                input.style.borderColor = `#ccc`; 
                input.style.boxShadow = `none`;
            }
        });
        if(allinputsFilled){
            GaussianElimination(inputNumbers);
        }
    });
}

function GaussianElimination(nums){
    let matrix = [];
    for(let i = 0;i< +selects[0].value;i++){
        let row = [];
        for(let j = 0;j< +selects[1].value;j++){
            row.push(nums[i * +selects[1].value + j]);    
        }
        matrix.push(row);
    }    
    rowEchelonForm(matrix);
    let solutions = ExtractSols(matrix);
    let sols = document.querySelector('#sols');
    if(sols.children.length > 0){
        sols.innerHTML = ``;
    }
    solutions.forEach((sol,index) => {
        let li = document.createElement('li');
        li.innerHTML = `x<sub>${index+1}</sub> = ${sol}`;
        sols.append(li);
    });
}

function rowEchelonForm(matrix) {
    let numRows = matrix.length; // Get the number of rows in the matrix
    let numCols = matrix[0].length; // Get the number of columns in the matrix
    let lead = 0; // Initialize the leading coefficient index to 0
  
    for (let r = 0; r < numRows; r++) { // Start looping through each row of the matrix
      if (lead >= numCols) {
        return; // If we've checked all columns, exit the function, we're done
      }
  
      let i = r;
  
      while (matrix[i][lead] === 0) { // Find the first row with a non-zero leading coefficient
        i++;
        if (i === numRows) { // If we've checked all rows for this column
          i = r; // Start checking the rows from the current row
          lead++; // Move to the next column
          if (lead === numCols) {
            return; // If we've checked all columns, exit the function, we're done
          }
        }
      }
  
      // Swap the rows if needed
      let temp = matrix[i];
      matrix[i] = matrix[r];
      matrix[r] = temp;
  
      // Normalize the pivot row
      let pivot = matrix[r][lead];
      for (let j = 0; j < numCols; j++) {
        matrix[r][j] /= pivot; // Make the leading coefficient 1
      }
  
      // Eliminate other rows
      for (let i = 0; i < numRows; i++) {
        if (i !== r) { // Skip the current row
          let factor = matrix[i][lead]; // Get the factor for row elimination
          for (let j = 0; j < numCols; j++) {
            matrix[i][j] -= factor * matrix[r][j]; // Eliminate elements below the leading coefficient
          }
        }
      }
  
      lead++; // Move to the next column
    }
  }
  
function ExtractSols(matrix){
    const numRows = matrix.length;
    const numCols = matrix[0].length - 1; // Excluding the last column

  const solutions = new Array(numCols).fill(0);
  for (let row = numRows - 1; row >= 0; row--) {
    let sum = 0;
    for (let col = row + 1; col < numCols; col++) {
      sum += matrix[row][col] * solutions[col];
    }
    solutions[row] = ((matrix[row][numCols] - sum) / matrix[row][row]).toFixed(2);
  }

  return solutions;
}