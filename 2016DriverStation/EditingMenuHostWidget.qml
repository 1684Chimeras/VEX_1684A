import QtQuick 2.0

Item {

    MouseArea{
        width: 9990;
        height: 8;
        id: mouseArea;
        hoverEnabled: true;
        property bool active: false;

        onPositionChanged: {
            if(active){
                if(mouse.y > 35){
                    active = false;
                }
            }else{
                active = true;
            }
        }

    }

    Item {
        id: content;

        y: -35;

        Rectangle{
            id: background;
            width: 9990;
            height: 35;
        }


    }


    states: [
        State{
            name: "Expanded"
            when: mouseArea.active
            PropertyChanges {
                target: content;
                y: 0;
            }

            PropertyChanges {
                target: mouseArea
                height: 9990;
                x: 10;
            }
        },State{

        }
    ]
    transitions: [Transition{
        NumberAnimation {
            property: "y";
            duration: 150;
            easing.type: Easing.InOutQuad
        }
    }]
}

