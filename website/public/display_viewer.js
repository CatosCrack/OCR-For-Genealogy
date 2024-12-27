document.addEventListener('DOMContentLoaded', async function() {
    
    // Get result ID
    const urlQuery = window.location.search;
    const params = new URLSearchParams (urlQuery);
    const id = params.get('id');
    const index = id.charAt(id.length-1);

    // Get image URL
    const results = JSON.parse(sessionStorage.getItem('results'));
    const imageURL = results[index]['url'];
    const bounds = results[index]['bounds'];

    console.log(bounds);

    const viewerDiv = document.createElement("div");
    viewerDiv.id = 'openseadragon';
    viewerDiv.style.backgroundColor = "black";
    document.body.appendChild(viewerDiv);

    var viewer = OpenSeadragon({
        id: "openseadragon",
        prefixUrl: "https://cdnjs.cloudflare.com/ajax/libs/openseadragon/4.0.0/images/",
        tileSources: {
            type: 'image',
            url: imageURL
        }
    });

    viewer.add

    const overlay = document.createElement('div');
    overlay.className = "bounding-box";
    overlay.style.position = "absolute";
    overlay.style.border = "2px solid red";

    overlay.style.left = bounds[0] + "%";
    overlay.style.top = bounds[1] + "%";
    overlay.style.width = bounds[2] + "%";
    overlay.style.height = bounds[3] + "%";

    viewer.addOverlay({
        element: overlay,
        location: new OpenSeadragon.Rect(bounds[0]/100, bounds[1]/100, bounds[2]/100, bounds[3]/100)
    });
});
