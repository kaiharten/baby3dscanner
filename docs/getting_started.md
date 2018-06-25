# Getting Started - Systeemhandleiding

## Maak verbinding met de Raspberry Pi

Plug een ethernet cabel in de raspberry pi en verbindt via SSH of maak verbinding via wifi en check het IP adres met ifconfig. Een VNC viewer kan ook worden gebruikt, dan is er een verbinding met GUI. Dit is niet noodzakelijk.

### Activeer de camera
Wanneer de raspberry pi opstart, moet dit weer opnieuw worden gedaan.

```sh
sudo modprobe bcm2835-v4l2
```

### Positioneer het Scanblok
Plaats de Raspberry Pi met Camera en Laser naar de zijkant van het frame aan de kant waar GEEN Touchscreen zit. Dit is de startpositie.

### Navigeer naar de map met het juiste python script
```sh
cd Documents/BSApp
```

### Start het Python script
```sh
python3 babyscanner.py
```

## De Applicatie

Druk op 'Start Scan' als het scanblok goed is gepositioneerd. Het systeem gaat dan scannen, door de motor te bewegen en foto's te maken.

Er komen statusberichten inbeeld 'Retreiving frame x of 140' en 'Processing frame x of 140'

Pas wanneer er weer done - idle staat kun je weer iets doen.

Beweeg de motor terug naar de start positie door "Back Home' te drukken.

## Matlab script

Open MATLAB en run het script op je laptop en controleer of het goed is gegaan door te kijken naar de grafieken. 

Zo ja? Ga naar de Raspberry Pi terug en klik op 'Go to Results' op de touchscreen.

Op dat scherm kun je op 'update' klikken om een nieuwe grafiek weer te geven van de afgelopen scan.

Vanuit hier kun je ook weer verder navigeren naar de 3D plot pagina en naar de scan pagina. 
