import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Controls.Styles 1.4
import "main.js" as SceneChanger
import "Auton"

Item {

    width: 1366;
    height: 566;
    Item{
        //Auton Selector

        Item {
            width: 260
            height: 500

            x: 40
            y: 566/2 - 250
            Item {
                id: dcHeader

                width: 260
                height: 56

                Rectangle{
                    width: 260
                    height: 56
                    color: "#aaaaff"
                }

                Label{
                    text: "Mode"
                    font.pixelSize: 36
                    y: 5
                    x: 10
                }
            }
            Item {
                y: 56
                width: 260
                x: 5
                height: 500 - 56
                Rectangle{
                    width: 260
                    x: -5
                    height: 500 - 56
                    color: "#ffffff"
                }

                ExclusiveGroup { id: tabPositionGroup }



                RadioButton {
                    y: 25
                    checked: true
                    style:  RadioButtonStyle {
                        label: Label{
                            text: "Not Selected"
                            font.pixelSize: 32
                        }
                    }
                    exclusiveGroup: tabPositionGroup
                }

                RadioButton {
                    y: 90
                    style:  RadioButtonStyle {
                        label: Label{
                            text: "Do Nothing"
                            font.pixelSize: 32
                        }
                    }
                    exclusiveGroup: tabPositionGroup
                }
                RadioButton {
                    y: 155
                    style:  RadioButtonStyle {
                        label: Label{
                            text: "Cross and Score"
                            font.pixelSize: 32
                        }
                    }
                    exclusiveGroup: tabPositionGroup
                }
                RadioButton {
                    y: 220
                    style:  RadioButtonStyle {
                        label: Label{
                            text: "Cross"
                            font.pixelSize: 32
                        }
                    }
                    exclusiveGroup: tabPositionGroup
                }
                RadioButton {
                    y: 285
                    style:  RadioButtonStyle {
                        label: Label{
                            text: "Score"
                            font.pixelSize: 32
                        }
                    }
                    exclusiveGroup: tabPositionGroup
                }
                RadioButton {
                    y: 350
                    style:  RadioButtonStyle {
                        label: Label{
                            text: "EXP- Two Ball"
                            font.pixelSize: 32
                        }
                    }
                    exclusiveGroup: tabPositionGroup
                }
            }
        }

    }
    function select(s){
        selectedLabel.text = "Selected: " + s;
        console.log(s)
    }

    Item{
        //Defense Selector
        width: 225
        height: 500
        x: 350
        y: 566/2 - 250

        Item {
            width: 225
            height: 56

            Rectangle{
                width: 225
                height: 56
                color: "#aaaaff"
            }

            Label{
                text: "Defense"
                font.pixelSize: 36
                y: 5
                x: 10
            }
        }

        Item {
            y: 56
            width: 225
            height: 500 - 56
            Rectangle{
                width: 225
                height: 500 - 56
                color: "#ffffff"
            }
            Label{
                text: "Selected: ¿por_que?"
                id: selectedLabel
                x: 15
                font.pixelSize: 18
            }

            ScrollView {
                width: 225;
                y: 24
                height: 500 - 56 - 24;
                Column {
                    width: 200;
                    height: 200 * 8;

                    DefenseTypeButton{
                        image: "ramparts"
                        onClick: select("ramparts")
                    }
                    DefenseTypeButton{
                        image: "cheval_de_frise"
                        onClick: select("cheval_de_frise")
                    }
                    DefenseTypeButton{
                        image: "drawbridge"
                        onClick: select("drawbridge")
                    }
                    DefenseTypeButton{
                        image: "moat"
                        onClick: select("moat")
                    }
                    DefenseTypeButton{
                        image: "portcullis"
                        onClick: select("portcullis")
                    }
                    DefenseTypeButton{
                        image: "rock_wall"
                        onClick: select("rock_wall")
                    }
                    DefenseTypeButton{
                        image: "rough_terrain"
                        onClick: select("rough_terrain")
                    }
                    DefenseTypeButton{
                        image: "sally_port"
                        onClick: select("sally_port")
                    }
                }
            }
        }
    }

    Item{
        //Defense Position Selector
        x: 620
        y: 566/2 - 250
        Item {
            width: 705
            height: 56

            Rectangle{
                width: 705
                height: 56
                color: "#aaaaff"
            }

            Label{
                text: "Position"
                font.pixelSize: 36
                y: 5
                x: 10
            }
        }

        Item {
            width: 705
            height: 500 - 56
            y: 56
            Rectangle{
                width: 705
                height: 500 - 56
                color: "#ffffff"
            }

            PositionSelectorWidget {

            }

        }
    }
}

