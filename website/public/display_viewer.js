document.addEventListener('DOMContentLoaded', function() {
    
    // Get result ID
    const urlQuery = window.location.search;
    const params = new URLSearchParams (urlQuery);
    const id = params.get('id');
    const index = id.charAt(id.length-1);

    // Get image URL
    const results = JSON.parse(sessionStorage.getItem('results'));
    const imageURL = results[index]['url'];
    const bounds = results[index]['bounds'];

    getImage(imageURL, bounds);

    const viewerDiv = document.createElement("div");
    viewerDiv.id = 'openseadragon';
    document.body.appendChild(viewerDiv);

    var viewer = OpenSeadragon({
        id: "openseadragon",
        prefixUrl: "https://cdnjs.cloudflare.com/ajax/libs/openseadragon/4.0.0/images/",
        tileSources: {
            type: 'image',
            //url: sessionStorage.getItem("image")
            url: imageURL
        }
    });

    viewer.add
});

async function getImage(imageURL, bounds) {
    try{
        const response = await fetch(imageURL);
        const blob = await response.blob();
        const reader = new FileReader();

        reader.onload = function() {
            const base64data = reader.result;
            sessionStorage.setItem("image", base64data);
        }

        reader.readAsDataURL(blob);

    } catch (error) {
        console.error(error);
    }
}