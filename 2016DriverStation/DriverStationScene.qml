import QtQuick 2.0
import QtQuick.Controls 1.4
//center : 350x350 circle
//edges - 800 long
//blue aura - FMS
//red aura - no Connection
//green aura - good connection
//angle of attack (focused upwards) - 250deg
//left third -
//top third - robot comms
//right third - code comms

Item {
    id: scene;
    width: 1366;
    height: 566;
    property double angle: 250;
    Label{
        text: "Theres nothing here?"
    }

    Item{
        id: auras;

        Item{
            id: redAura;
        }

        Item{
            id: blueAura;

        }

        Item{
            id: greenAura;
        }
    }

    Item{
        id: center;

        Image{
            id: circle;
        }

        MouseArea{

        }

    }

    Item{
        id: edges;
    }

}

