function addSkill(element) {
    request = new XMLHttpRequest();
    url = "skillup?skill=" + element;
    request.open('GET', url);
    request.setRequestHeader('Content-Type', 'application/x-www-form-url');
    request.addEventListener("readystatechange", () => {
        if (request.readyState === 4 && request.status === 200) {
            json = JSON.parse(request.responseText);
            if (json[0] == "ok")
                document.getElementById("perk").innerHTML = json[1];
        }
    })
    request.send();
}

document.addEventListener('DOMContentLoaded', function() {
    var el = document.getElementsByClassName("skillup");
    for (i = 0; i < el.length; i++)
        el[i].addEventListener("click", function(e) { addSkill(e.currentTarget.attributes["data-skill"].value) }, false);
})