function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) { return false;}
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
          /*check if the item starts with the same letters as the text field value:*/
          if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
            /*create a DIV element for each matching element:*/
            b = document.createElement("DIV");
            /*make the matching letters bold:*/
            b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
            b.innerHTML += arr[i].substr(val.length);
            /*insert a input field that will hold the current array item's value:*/
            b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
            /*execute a function when someone clicks on the item value (DIV element):*/
            b.addEventListener("click", function(e) {
                /*insert the value for the autocomplete text field:*/
                inp.value = this.getElementsByTagName("input")[0].value;
                /*close the list of autocompleted values,
                (or any other open lists of autocompleted values:*/
                closeAllLists();
            });
            a.appendChild(b);
          }
        }
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
          /*If the arrow DOWN key is pressed,
          increase the currentFocus variable:*/
          currentFocus++;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 38) { //up
          /*If the arrow UP key is pressed,
          decrease the currentFocus variable:*/
          currentFocus--;
          /*and and make the current item more visible:*/
          addActive(x);
        } else if (e.keyCode == 13) {
          /*If the ENTER key is pressed, prevent the form from being submitted,*/
          e.preventDefault();
          if (currentFocus > -1) {
            /*and simulate a click on the "active" item:*/
            if (x) x[currentFocus].click();
          }
        }
    });
    function addActive(x) {
      /*a function to classify an item as "active":*/
      if (!x) return false;
      /*start by removing the "active" class on all items:*/
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = (x.length - 1);
      /*add class "autocomplete-active":*/
      x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
      /*a function to remove the "active" class from all autocomplete items:*/
      for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
      }
    }
    function closeAllLists(elmnt) {
      /*close all autocomplete lists in the document,
      except the one passed as an argument:*/
      var x = document.getElementsByClassName("autocomplete-items");
      for (var i = 0; i < x.length; i++) {
        if (elmnt != x[i] && elmnt != inp) {
          x[i].parentNode.removeChild(x[i]);
        }
      }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
  }
  
  /*An array containing all the division names in the world:*/
  var division = ['BILOB (10029)', 'BIMB Invest (10030)', 'BIMB Investment Mgt Bhd (30001)', 'BIMB Securities Sdn Bhd (60001)', 'BIMB Solutions (40001)', 'Branch Operations & Supervision (10034)', 'Branches (10033)', 'Brand & Marketing Communication (10001)', 'Business Marketing (10001)', 'Business Support (10002)', "Chief Operating Officer's Office (10018)", 'Commercial Banking (10005)', 'Commercial Client Solutions (10005)', 'Compliance (10006)', 'Consumer Banking (10007)', 'Corporate Banking (10008)', 'Corporate Support (10009)', 'Credit Management (10010)', 'Deposit & Cards (10011)', 'Deposit & Cash Management (10011)', 'E-Channels (10035)', 'Farihan Corporation (40001)', 'Finance (10012)', 'Financing Solutions (10008)', "Group Chief Business Officer's Office - Group Institutional Banking (10038)", "Group Chief Business Officer's Office - Retail (10003)", "Group Chief Credit Officer's Office (10010)", "Group Chief Executive Officer's Office (10004)", "Group Chief Operating Officer's Office (10018)", 'Group Compliance (10006)', 'Group Corporate Communications (10013)', 'Group Credit Management (10010)', 'Group Digital (10024)', 'Group Finance (10012)', 'Group Financial Inclusion (10025)', 'Group Human Resources (10014)', 'Group Information Security & Governance (10015)', 'Group Internal Audit (10016)', 'Group Legal and Secretarial (10017)', 'Group Retail Banking (10003)', 'Group Risk Management (10021)', 'Group Shariah (10022)', 'Group Strategic Management (10024)', 'Group Technology (10026)', 'Human Resources', 'Information Security & Governance', 'Information Security & Governance (10015)', 'N/A', 'Non Retail Special Assets Management (10020)', 'Product Management (10019)', 'Recovery & Rehabilitation (10020)', 'Retail Assets (10039)', 'Retail Banking Distribution (10007)', 'Risk Management (10021)', 'SME Banking (10023)', 'Strategic Management (10024)', 'Strategic Relations (10025)', 'Strategy & Centralized Services (10040)', 'Technology (10026)', 'Technology Services (10026)', 'Treasury & Markets (10027)', 'Treasury (10027)', 'Wealth Management (10036)'];
  
  /*initiate the autocomplete function on the "myInput" element, and pass along the division array as possible autocomplete values:*/
  autocomplete(document.getElementById("divisionInput"), division);