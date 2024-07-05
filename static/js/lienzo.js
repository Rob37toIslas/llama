
const canvas = new fabric.Canvas("canvas", {
    width: 1200,
    height: 450,
    backgroundColor: "#fff",
    erasable: false,
  });
var ctx = canvas.getContext("2d");
var color = "#000";




function Copy() {
  canvas.getActiveObject().clone(function (cloned) {
    _clipboard = cloned;
  });
}

function Cut() {
  Copy();
  eliminar();
}

function Paste() {
  _clipboard.clone(function (clonedObj) {
    canvas.discardActiveObject();
    clonedObj.set({
      left: clonedObj.left + 10,
      top: clonedObj.top + 10,
      evented: true,
    });
    if (clonedObj.type === "activeSelection") {
      clonedObj.canvas = canvas;
      clonedObj.forEachObject(function (obj) {
        canvas.add(obj);
      });
      clonedObj.setCoords();
    } else {
      canvas.add(clonedObj);
    }
    _clipboard.top += 10;
    _clipboard.left += 10;
    canvas.setActiveObject(clonedObj);
    canvas.requestRenderAll();
  });
}

function eliminar() {
  var Obj = canvas.getActiveObject();
  if (Obj.type === "activeSelection") {
    Obj.canvas = canvas;
    Obj.forEachObject(function (obj) {
      canvas.remove(obj);
    });
  } else {
    var activeObject = canvas.getActiveObject();
    if (activeObject !== null) {
      canvas.remove(activeObject);
    }
  }
}

document.addEventListener("keydown", function (e) {
  if (e.ctrlKey && e.code === "KeyC") {
    Copy();
  } else if (e.ctrlKey && e.code === "KeyV") {
    Paste();
  } else if (e.ctrlKey && e.code == "KeyX") {
    Cut();
  } else if (e.code == "Delete") {
    eliminar();
  }
  
});




const circulo = document.getElementById("circulo")
circulo.addEventListener("click",async (e)=>{
  e.preventDefault();
  try{
      canvas.add( 
        new fabric.Circle({ 
          radius: 30, 
          fill: 'transparent',
          stroke: color,
          top: 100, 
          left: 100 
        })
        );
  }catch(error){
    console.log(error)
  }

});
const cuadrado =document.getElementById("cuadrado")
cuadrado.addEventListener("click",async(e)=>{
  e.preventDefault();
  try{
    canvas.add(
      new fabric.Rect({
          top: 100, 
          left: 0, 
          width: 80, 
          height: 80, 
          fill: 'transparent',
          stroke: color,
        })
      );
  }catch(error){
    console.log(error)
  }
});

const triangulo =document.getElementById("triangulo");
triangulo.addEventListener("click",async(e)=>{
  e.preventDefault();
  try{
    canvas.add(
      new fabric.Triangle({
        width: 100, 
        height: 70, 
        fill: 'transparent',
        stroke:color, 
        left: 50, 
        top: 50
      })
    )
  }catch(error){
    console.log(error)
  }
});

const paleta = document.getElementById("paleta");
const col = document.getElementById("color");
col.addEventListener("input", async (e)=> {
  e.preventDefault()
  try{
    color = col.value;
    paleta.style.color = color;

  var obj =canvas.getActiveObject().type;
  if(obj == 'path'){
    canvas.getActiveObject().set('stroke',color);
  }else if (obj === 'rect' || obj === 'circle' || obj === 'triangle') {
      canvas.getActiveObject().set('stroke', color);
  }else if (obj == ''){
      console.log('hola')
  }
  }catch(error){
    console.log(error)
  }
});

const goma = document.getElementById("goma");
goma.addEventListener("click",async(e)=>{
  e.preventDefault();
  try{
      canvas.freeDrawingBrush = new fabric.EraserBrush(canvas);
      canvas.isDrawingMode = !canvas.isDrawingMode;
      canvas.freeDrawingBrush.width = 10;
  }catch(error){
    console.log(error)
  }
});
const revertir = document.getElementById("revertir");
revertir.addEventListener("click",async(e)=>{
  e.preventDefault();
  try{
    canvas.freeDrawingBrush = new fabric.EraserBrush(canvas);
    canvas.isDrawingMode = !canvas.isDrawingMode;
    console.log(canvas.isDrawingMode)
    canvas.freeDrawingBrush.width = 10;
    canvas.freeDrawingBrush.inverted = true;
  }catch(error){
    console.log(error)
  }
});

const pincel =document.getElementById("pincel")
pincel.addEventListener("click", async (e) => {
  e.preventDefault();
  try {
    canvas.freeDrawingBrush = new fabric.PencilBrush(canvas);
    canvas.isDrawingMode = !canvas.isDrawingMode;
    canvas.freeDrawingBrush.color = color;

  } catch (error) {
    console.log(error);
  }
});


   
const limpiar = document.querySelector("#limpiar");
limpiar.addEventListener("click", async (e) => {
  e.preventDefault();
  try {
    canvas.clear();
    canvas.setBackgroundColor('#fff');
    canvas.renderAll();
  } catch (error) {
    console.log(error);
  }
});


function save(name){
  const dataURL = canvas.toDataURL({ format: 'jpeg', quality: 0.8 });
  const link = document.createElement('a');
  link.href = dataURL;
  link.download = name+'.jpg';
  link.click();
}





