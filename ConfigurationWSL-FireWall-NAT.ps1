# Pour ajouter un script au démarrage de la machine windows
# https://www.it-connect.fr/parametrer-le-lancement-dun-script-a-larret-ou-au-demarrage-de-windows-pro/


# Vérifier que l'exécution de scripts Powershell est autorisée:

# Ouvrez Powershell en administrateur, puis tapez:
# Get-ExecutionPolicy
# Doit renvoyer Unrestricted

# Sinon, tapez:
# Set-ExecutionPolicy Unrestricted
# Validez par O





<#

 ____                       _ _       
/ ___|  ___  ___ _   _ _ __(_) |_ ___ 
\___ \ / _ \/ __| | | | '__| | __/ _ \
 ___) |  __/ (__| |_| | |  | | ||  __/
|____/ \___|\___|\__,_|_|  |_|\__\___|


On va faire en sorte que le script soit exécuté en administrateur
#>
if (-Not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')) {
    if ([int](Get-CimInstance -Class Win32_OperatingSystem | Select-Object -ExpandProperty BuildNumber) -ge 6000) {
        $Command = "-File `"" + $MyInvocation.MyCommand.Path + "`" " + $MyInvocation.UnboundArguments
        Start-Process -FilePath PowerShell.exe -Verb RunAs -ArgumentList $Command
        Exit
 }
}



<#

    _       _                             ___ ____                            __        ______  _     
   / \   __| |_ __ ___  ___ ___  ___     |_ _|  _ \                           \ \      / / ___|| |    
  / _ \ / _` | '__/ _ \/ __/ __|/ _ \_____| || |_) |____ _____ _____ _____ ____\ \ /\ / /\___ \| |    
 / ___ \ (_| | | |  __/\__ \__ \  __/_____| ||  __/_____|_____|_____|_____|_____\ V  V /  ___) | |___ 
/_/   \_\__,_|_|  \___||___/___/\___|    |___|_|                                 \_/\_/  |____/|_____|
       

Récupérer l'adresse IP de la machine Linux WSL                                                                                               
Attention, ici la WSL se nomme Debian (vérifiez avec wsl -l -v)
#>
$wsl_address = wsl -d Debian hostname -I
$found       = $wsl_address -match '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}';

# On arrête si aucune WSL n'est détectée
if( $found ){
  $wsl_address = $matches[0];
} else{
  echo "Le script va se fermer car l'adresse IP de la machine WSL 2 est introuvable.";
  exit;
}



<#

__     __         _       _     _           
\ \   / /_ _ _ __(_) __ _| |__ | | ___  ___ 
 \ \ / / _` | '__| |/ _` | '_ \| |/ _ \/ __|
  \ V / (_| | |  | | (_| | |_) | |  __/\__ \
   \_/ \__,_|_|  |_|\__,_|_.__/|_|\___||___/
                                           

#>
# Tous les ports à forwarder vers votre machine WSL 2
$ports     = @(80, 21, 63000);

# Adresse IP sur laquelle écouter au niveau de la machine Windows 10
$addr      ='0.0.0.0'; # Correspond à toutes les interfaces réseau de la machine hôte
$ports_a   = $ports -join ",";



<#

 ____            _                 _____ _                        _ _ 
|  _ \ ___  __ _| | ___  ___      |  ___(_)_ __ _____      ____ _| | |
| |_) / _ \/ _` | |/ _ \/ __|_____| |_  | | '__/ _ \ \ /\ / / _` | | |
|  _ <  __/ (_| | |  __/\__ \_____|  _| | | | |  __/\ V  V / (_| | | |
|_| \_\___|\__, |_|\___||___/     |_|   |_|_|  \___| \_/\_/ \__,_|_|_|
           |___/                                                      

#>
# Supprimer la règle de pare-feu "WSL 2 Firewall Unlock"
iex "Remove-NetFireWallRule -DisplayName 'WSL 2 Firewall Unlock' ";


# Créer les règles de pare-feu (flux entrant et sortant) avec chacun des ports de $ports
iex "New-NetFireWallRule -DisplayName 'WSL 2 Firewall Unlock' -Direction Outbound -LocalPort $ports_a -Action Allow -Protocol TCP";
iex "New-NetFireWallRule -DisplayName 'WSL 2 Firewall Unlock' -Direction Inbound -LocalPort $ports_a -Action Allow -Protocol TCP";





<#
 ____            _                       _   _    _  _____ 
|  _ \ ___  __ _| | ___  ___            | \ | |  / \|_   _|
| |_) / _ \/ _` | |/ _ \/ __|_____ _____|  \| | / _ \ | |  
|  _ <  __/ (_| | |  __/\__ \_____|_____| |\  |/ ___ \| |  
|_| \_\___|\__, |_|\___||___/           |_| \_/_/   \_\_|  
           |___/                                           

#>
# Créer les règles de redirection de ports (NAT) pour chacun des ports ($ports)
for( $i = 0; $i -lt $ports.length; $i++ )
{
  $port = $ports[$i];

  # D'abord, on supprime les éventuelles restes de précédentes règles
  iex "netsh interface portproxy delete v4tov4 listenport=$port listenaddress=$addr";

  # On ajoute ensuite la bonne règle
  iex "netsh interface portproxy add v4tov4 listenport=$port listenaddress=$addr connectport=$port connectaddress=$wsl_address";
}