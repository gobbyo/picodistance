# Assembly

You'll need to 3d print the casing, order your printed circuit board, and have all your parts from the parts list before you can successfully assemble this project.

## Printed circuit board (PCB)
Ordering a PCB only requires the [gerber file](..\pcb\Gerber_PCB_DistanceMeasure.zip) found in this GitHub repository. Note that you should get a few price quotes before ordering your PCB.  Some PCB fabrication sites require the PCB's overall dimensions to obtain a price quote, see the image below detailing its dimensions. Note that some sites will extract the PCB's dimensions directly from the gerber file. If you are uncomfortable soldering the components to the PCB, then consider having the PCB fabrication assemble the board for you.
:::image type="content" source="images/pcbdimensions.png" alt-text="PCB Dimensions":::
PCB Dimensions

Most PCB fabricators require a minimum order of around 5 boards. This board is a simple 2 layer PCB--top and bottom, see images below.

:::image type="content" source="images/pcbtop.png" alt-text="Top view of PCB":::
Top view of the PCB

:::image type="content" source="images/pcbbottom.png" alt-text="Bottom view of PCB":::
Bottom view of the PCB

Be sure to shop around before ordering your PCB as there is quite a price difference across various PCB fabricators. Below is a list of various fabricators:

## Casing and Component Mounting

The casing comes in two parts, the front and back. You can use any flavor of filament, PLA works fine.  It is best to print the top a different color from the bottom. That way the physical buttons that initiate the ultrasonic measurement can easily be associated with the front or back.

## Wiring

## Microcontroller installation and updates

The code for this project is written using Micropython.

## Verify functionality