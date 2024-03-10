// Initialize and add the map
let map;

async function initMap() {
  // The location of Uluru
  const position = { lat: 50.73616692515237, lng: -3.5334316093373945 };
  // Request needed libraries.
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // The map, centered at Uluru
  map = new Map(document.getElementById("map"), {
    zoom: 16,
    center: position,
    mapId: "campus",
  });

  const SportsParkTag = document.createElement("div");

  SportsParkTag.className = "name-tag";
  SportsParkTag.textContent = "Sports Park";

  const SPmarker = new AdvancedMarkerElement({
    map,
    position: { lat: 50.73781086413985, lng: -3.5369991064472885 },
    content: SportsParkTag,
  });
  

  const LaverBuildingTag = document.createElement("div");

  LaverBuildingTag.className = "name-tag";
  LaverBuildingTag.textContent = "Laver Building";

  const LBmarker = new AdvancedMarkerElement({
    map,
    position: { lat: 50.7375072917037, lng: -3.5334938730196983 },
    content: LaverBuildingTag,
  });


  const ForumLibraryTag = document.createElement("div");

  ForumLibraryTag.className = "name-tag";
  ForumLibraryTag.textContent = "Forum Library";

  const FLmarker = new AdvancedMarkerElement({
    map,
    position: { lat: 50.7352855459596, lng: -3.5333676503524343 },
    content: ForumLibraryTag,
  });


  const ReedPondTag = document.createElement("div");

  ReedPondTag.className = "name-tag";
  ReedPondTag.textContent = "Reed Pond";

  const RPmarker = new AdvancedMarkerElement({
    map,
    position: { lat: 50.734399309503075, lng: -3.5375457289062844 },
    content: ReedPondTag,
  });


  const EastParkTag = document.createElement("div");

  EastParkTag.className = "name-tag";
  EastParkTag.textContent = "East Park";

  const EPmarker = new AdvancedMarkerElement({
    map,
    position: { lat: 50.73764355152051, lng: -3.527791142400209 },
    content: EastParkTag,
  });
}

initMap();