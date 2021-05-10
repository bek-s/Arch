function buyMarket(id) {
    request = new XMLHttpRequest();
    count = document.getElementById("input_count_for_"+id).value;
    url = "buy?id=" + id +"&count=" + count;
    request.open('GET', url);
    request.setRequestHeader('Content-Type', 'application/x-www-form-url');
    request.addEventListener("readystatechange", () => {
        if (request.readyState === 4 && request.status === 200) {
            json = JSON.parse(request.responseText);
            if (json[0] == "ok"){
                document.getElementById("market_items").innerHTML = json[1];
                reload_buy_Listeners();
                alert("Куплено");
                }
            else{
                alert("Ошибка покупки");
            }

        }
    })
    request.send();
}

function newMarket() {
    request = new XMLHttpRequest();
    id_item1 =document.getElementById("item1_select").value;
    id_item2 =document.getElementById("item2_select").value;
    count = document.getElementById("input_counnt_item1").value;
    cost=document.getElementById("input_cost_item2").value;
    url = "new_market?item=" + id_item1 +"&count=" + count +"&item2="+id_item2+"&cost="+cost;
    request.open('GET', url);
    request.setRequestHeader('Content-Type', 'application/x-www-form-url');
    request.addEventListener("readystatechange", () => {
        if (request.readyState === 4 && request.status === 200) {
            json = JSON.parse(request.responseText);
            if (json[0] == "ok"){
                document.getElementById("item1_select").value = "";
                document.getElementById("item2_select").value = "";
                document.getElementById("input_counnt_item1").value = "";
                document.getElementById("input_cost_item2").value = "";
                alert(json[1]);
                }
            else{
                alert(json[1]);
            }

        }
    })
    request.send();
}

document.addEventListener('DOMContentLoaded', function() {
    var el = document.getElementsByClassName("buy_button");
    for (i = 0; i < el.length; i++)
        el[i].addEventListener("click", function(e) { buyMarket(e.currentTarget.attributes["data-id"].value) }, false);
})

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("new_market").addEventListener("click", function(e)
    { newMarket() }, false);
})

function reload_buy_Listeners(){
    var el = document.getElementsByClassName("buy_button");
    for (i = 0; i < el.length; i++)
        el[i].addEventListener("click", function(e) { buyMarket(e.currentTarget.attributes["data-id"].value) }, false);
}