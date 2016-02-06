import QtQuick 2.0
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
    property double angle: 250;

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

