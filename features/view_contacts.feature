Feature: Visa kontaktsidan

  Scenario: Användaren är på rätt sida
    Given att användaren öppnar kontaktsidan
    Then ska webbadressen vara "https://forverkliga.se/JavaScript/my-contacts/#/"



  Scenario: Användaren kan klicka på Vänlista
    Given att användaren öppnar startsidan
    When användaren klickar på knappen "Vänlista"
    Then ska användaren se vänlistan

    

  Scenario: Användaren lägger till en ny vän via "Ny vän"-formuläret
  Given att användaren öppnar startsidan
  When användaren klickar på knappen "Ny vän"
  And användaren fyller i namn med "Luke Skywalker"
  And användaren fyller i e-post med "luke.skywalker@rebelalliance.org"
  And användaren klickar på knappen "Spara"
  Then ska användaren se meddelandet "Fyll i båda fälten för att lägga till din vän." visas inte
  And den nya vännen "Luke Skywalker" ska synas i listan
