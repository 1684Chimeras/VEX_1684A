.pragma library;

var winder;
var contint;
console.log("Init!")

function setWindow(window, content){
    console.log("Winder : " + window);
    winder = window;
    contint = content;
}

function to(s){
    //console.log("Hello! " + s);

    for(var i = 0; contint.children.length > i; i++) {
       // console.log("Wattson? " + i);
        contint.children[i].destroy();
    }
    //console.log("Size : " + contint.children.length)
    var component = Qt.createComponent(s + ".qml");
    var sprite = component.createObject(contint, {"x": 0, "y": 0});
   // print("NOTHING IS HAPPPPPPPPPPPENING")
}
