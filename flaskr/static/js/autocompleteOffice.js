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

/*An array containing all the office names in the world:*/
var office = ['Admin Audit (1160005)', 'Alternative Channel (1070011)', 'AML/CFT (1060003)', 'Ar-Rahnu (1390005)', 'Asset Liability & Information Management (1400006)', 'Asset Quality Management & Review (1230002)', 'B.Solutions-Collections Call Centre (4010001)', 'B.Solutions-Sale (4010002)', 'B.Solutions-Transactional (HQ) (4010006)', 'BICC- Card Operation (1020003)', 'BIMB Investment Management Berhad (1300001)', 'BIMB Labuan Offshore (1290001)', 'BOD B.Solutions (4010004)', 'BOD Farihan (4010004)', 'BOD Investment (3010008)', 'BOD legal (1170004)', 'BOD Securities (6010010)', 'Br Alamesra (1333098)', 'Br Alor Setar (1333004)', 'Br Ampang (1333092)', 'Br Ara damansara (1333124)', 'Br Austin Height (1333143)', 'Br Ayer Keroh (1333116)', 'Br Bagan Serai (1333075)', 'Br Baling (1333032)', 'Br Bandar Baru Tunjung (1333132)', 'Br Bandar Botanic Klang (1333117)', 'Br Bandar Kinrara (1333128)', 'Br Bandar Muazam Shah (1333070)', 'Br Bandar Penawar (1333111)', 'Br Bandar Pusat Jengka (1333039)', 'Br Bandar Sri Damansara (1333137)', 'BR Bandar Tasik Permaisuri (1333121)', 'Br Bandar Wawasan (1333081)', 'Br Bangi (1333019)', 'Br Bangi 2 (1333147)', 'Br Banting (1333038)', 'Br Batu Pahat (1333023)', 'Br Bayan Baru (1333063)', 'Br Bintulu (1333048)', 'Br Bukit Damansara (1333102)', 'Br Bukit Indah (1333130)', 'Br Bukit Jelutong (1333127)', 'Br Butterworth (1333005)', 'Br Chukai (1333022)', 'Br Cyberjaya (1333126)', 'Br Denai Alam (1333144)', 'Br Dungun (1333034)', 'Br Georgetown (1333057)', 'Br Gua Musang (1333059)', 'Br Guar Chempedak (1333073)', 'Br Ipoh (1333014)', 'Br Jalan Raja Syed Alwi (1333012)', 'Br Jalan Tun Razak (1333010)', 'Br Jasin (1333041)', 'Br Jerantut (1333069)', 'Br Jerteh (1333029)', 'Br Jitra (1333031)', 'Br Johor Bahru (1333015)', 'Br Kajang (1333065)', 'Br Kelana Jaya (1333093)', 'Br Keningau (1333142)', 'Br Kepala Batas (1333062)', 'Br KL Sentral (1333007)', 'Br Klang (1333006)', 'Br Kluang (1333036)', 'Br Kodiang (1333145)', 'Br Kota Bharu (1333080)', 'Br Kota Damansara (1333095)', 'Br Kota Kinabalu (1333016)', 'Br Kota Samarahan (1333077)', 'Br Kota Tinggi (1333040)', 'Br Kuala Krai (1333046)', 'Br Kuala Nerus (1333141)', 'Br Kuala Pilah (1333049)', 'Br Kuala Terengganu (1333002)', 'Br Kuantan (1333009)', 'Br Kubang Kerian (1333003)', 'Br Kuching (1333013)', 'Br Kulaijaya (1333108)', 'Br Kulim (1333043)', 'Br Labuan (1333051)', 'Br Lahad Datu (1333076)', 'Br Langkawi (1333072)', 'Br Machang (1333044)', 'Br Masjid Tanah (1333035)', 'Br Medan MARA (1333017)', 'Br Melaka (1333011)', 'Br Melawati (1333079)', 'Br Menara Bank Islam (1333001)', 'Br Menara TM (1333086)', 'Br Mersing (1333053)', 'Br Meru Raya (1333125)', 'Br Miri (1333054)', 'Br Muar (1333027)', 'Br Nilai (1333061)', 'Br Padang Garong (1333136)', 'Br Padang Hiliran (1333104)', 'Br Parit Buntar (1333021)', 'Br Pasir Gudang (1333066)', 'Br Pasir Mas (1333024)', 'Br Pasir Puteh (1333078)', 'Br Pasir Tumboh (1333123)', 'Br Pekan (1333087)', 'Br Perda (1333090)', 'Br Persiaran Sultan Abdul Hamid (1333103)', 'Br Petaling Jaya (1333026)', 'Br Petaling Jaya New Town (1333109)', 'Br Pokok Sena (1333050)', 'Br Pontian (1333084)', 'Br Port Dickson (1333047)', 'Br Putra Height (1333096)', 'Br Putra Square (1333097)', 'Br Putrajaya (1333083)', 'Br Raub (1333068)', 'Br Rawang (1333107)', 'Br Rompin (1333122)', 'Br Sandakan (1333094)', 'Br Saujana Utama (1333101)', 'Br Segamat (1333058)', 'Br Sek 18 Shah Alam (1333114)', 'Br Selayang (1333074)', 'Br Semarak (1333113)', 'Br Semenyih (1333106)', 'Br Senawang (1333134)', 'Br Seremban (1333008)', 'Br Seri  Iskandar (1333091)', 'Br Setia Alam (1333148)', 'Br Shah Alam (1333025)', 'Br Sibu (1333129)', 'Br Sik (1333150)', 'Br Simpang Tiga (1333110)', 'Br Sri Gombak (1333115)', 'Br Sri Manjung (1333042)', 'Br Sri Petaling (1333112)', 'Br Subang Jaya (1333037)', 'Br Sungai Besar (1333052)', 'Br Sungai Buloh (1333131)', 'Br Sungai Limau (1333151)', 'Br Sungai Petani (1333018)', 'Br Sungai Petani 2 (1333135)', 'Br Taiping (1333055)', 'Br Taman Tun Dr Ismail (1333088)', 'Br Tampin (1333028)', 'Br Tampoi (1333064)', 'Br Tanah Merah (1333033)', 'Br Tanjung Karang (1333060)', 'Br Tanjung Malim (1333045)', 'Br Tawau (1333030)', 'Br Teluk Intan (1333056)', 'Br Temerloh (1333020)', 'Br UIA Gombak (1333082)', 'Br UITM Shah Alam (1333118)', 'Br Universiti Malaya (1333085)', 'Br Universiti Utara Malaysia (1333089)', 'Br Wakaf Bharu (1333140)', 'Br Wangsa Maju (1333099)', 'Branch & Regional Support (1340008)', 'Branch Audit (1160002)', 'Branch Operations (1340002)', 'Branch Process Improvement (1340004)', 'Branch Supervision & Support (1340003)', 'Branch Supervision (1340003)', 'Brand & Marketing Communication (1010001)', 'Bureau De Change (1270001)', 'Business (1050001)', 'Business (Corporate) (1110003)', 'Business (Retail) (1110007)', 'Business 2 (1080002)', 'Business Analytics (1070003)', 'Business Analytics (1400003)', 'Business Continuity (1210001)', 'Business Corporate – Wholesale (1110003)', 'Business Development (1230003)', 'Business Development – Retail (1110008)', 'Business Finance & Analytics (1120001)', 'Business Operations & Governance (1380003)', 'Business Performance Management (1050002)', 'Business Review (1360001)', 'Business Services (1110011)', 'Business Strategis,MIS&Admin (1110006)', 'Business Strategy & Development (1360003)', 'Business Strategy (1030001)', 'CAFIB (1210003)', 'Capital & Balance Sheet management (1120002)', 'Capital Markets (1270005)', 'Card Business (1110010)', 'Card Operations (1020003)', 'Card Operations and Card Business (1020003)', 'CDX (1240003)', 'Central Financing Processing Centre (1100004)', 'Centralized Procurement (1120005)', 'Centralized Transaction & Agent Banking (1340009)', 'Centralized Transaction Unit (1340009)', "CEO's Office (3010002)", 'Change Value Management (1070010)', 'Chief Economist Department (1040002)', "Chief Executive's Office (1040001)", 'Climate Risk Department (1210009)', 'Commercial Client Solutions (1050006)', 'Commercial Financing Solutions (1080004)', 'Compliance (3010003)', 'Compliance Academy & Policy (1060009)', 'Compliance Academy, Policy & Strategy (1060009)', 'Compliance Advisor (1060004)', 'Compliance Monitoring & Testing (1060002)', 'Consumer Business Development (1070007)', 'Consumer Business Support (1070003)', 'Consumer Collection Dept (1200002)', 'Consumer Products Management (1070007)', 'Consumer Recovery Dept (1200003)', 'Consumer Sales Management (1070002)', 'Contact Center and Customer Care (1180002)', 'Contact Centre (1010002)', 'Corporate Financing Solutions (1050005)', 'Corporate Governance Dept (6010007)', 'Corporate Secretarial (1170003)', 'Credit Administration (1020001)', 'Credit Analysis (1100002)', 'Credit Assessment & Review (1230004)', 'Credit AUDIT (1160001)', 'Credit Management Control (1100001)', 'Credit Post-Approval (1210007)', 'Credit Risk Portfolio Management (1210004)', 'Credit Support (1080005)', "CRO's Office (1210006)", 'Culture & Learning (1140004)', 'Culture & People Development', 'Customer Experience & Governance (1350004)', 'Customer Experience (CX) (1350005)', 'Customer Service Quality (1340005)', 'Cybersecurity (1150002)', 'Data Analytics (1240005)', 'Data Governance (1150003)', 'Data Management (1080006)', 'Deputy Treasurer1 (1270003)', 'Digital Transformation (1240002)', 'Distribution Channel (1070002)', 'Embedded Risk & Compliance (1340007)', 'Embedded Risk (1340015)', 'Embedded Risk Unit (1250005)', 'Employee Experience', 'ESG (1100006)', 'Farihan-Ar-Rahnu (4010003)', 'Farihan-Collections Call Centre (4010001)', 'Farihan-Sale (4010002)', 'Farihan-Transactional (HQ) (4010006)', 'Finance & Operations (3010005)', 'Finance & Support Services (1290002)', 'Finance & Support Services (SABAH) (1290003)', 'Finance Operations (1120004)', 'Finance, Human Resource \n& Administration Dept (6010006)', 'Financial Crime & Regulatory Compliance (1060003)', 'Financial Crime Compliance (1060003)', 'Financial Reporting (1120003)', 'Fundrising & Inclusions (1250004)', 'General Administration (1120006)', 'Government & Corporate Client Solutions (1380006)', 'Group Corporate Communications (1130001)', "Head of Division's Office (1140001)", 'Head Of Regional Office (1070008)', 'House & Fixed Financing (1390002)', 'HR Culture &Capability Development (1140004)', 'HR Project, Policy & Compliance (1140005)', 'HRBP (1140007)', 'Human Resource (3010006)', 'IFiC Banda Kaba (1333146)', 'Industrial Relations & Performance Management Development (1140002)', 'Information Security & Governance', 'Innovation, data & Compliance (1250004)', 'Institutional & Corporate Business (3010010)', 'Institutional Dealing Dept (6010001)', 'Integrity & Governance (1060007)', 'Internet & Mobile (1350003)', 'Investigation & Control (1340006)', 'Investment (3010007)', 'Investment Banking & Advisory (1380004)', 'Investor Sales (1270006)', 'IT Applications (1260008)', 'IT Audit (1160004)', 'IT Blueprint – Enterprise Architecture (1260010)', 'IT Data Management Unit (1260001)', 'IT Embedded Risk Unit (1260002)', 'IT Infrastructure (1260007)', 'IT Infrastructure Management (1260007)', 'IT Operation (1260003)', 'IT Planning & Innovation (1260005)', 'IT Security (1260009)', 'IT Strategy & Planning (1260005)', 'IT Transformation Management Office (TMO) (30ITD12)', 'Legal & Credit Dept (6010005)', 'Legal (1170002)', 'Legal and Secretarial (1170001)', 'Liquidity Management Channel (1380001)', 'Market Risk Management (1210002)', 'Marketing And Technology (1110004)', 'N/A', 'Non-Retail Special Assets Management (1100008)', 'Operational Risk Management & Business Continuity Management (1210001)', 'Operations & Fulfillment (1360002)', 'Operations & IT Dept (6010004)', 'Operations (1340012)', 'Operations (3010012)', 'Organisation & Methods (1180001)', 'Payments & SST (1350002)', 'Personal Financing (1390003)', 'Planning & Sustainability (1040003)', 'PMO - Retail Assets (1390001)', 'PMO Deposit & Cards (1110009)', 'PMO Retail Banking Distribution (1070009)', 'Portfolio Management (1270008)', 'Product & System Support (1190002)', 'Product Management (1190001)', 'Product-Deposit & Business Solution (1110002)', 'Programme Management Office (1260006)', 'Project, Strategy & Innovation (1230006)', 'Projects and Task Force Unit (1340010)', 'Property and Project Management (1120007)', 'Recons & Support (1340013)', 'Recovery & Rehabilitation (1200001)', 'Regional Control (1340008)', 'Regional Directors (1070008)', 'Regional Monitoring (1340008)', 'Regulatory Compliance (1060006)', 'Remittance Services & Correspondent Banking (1340014)', 'Reporting & Credit Analytics (1100003)', 'Research and  Advisory (1220001)', 'Research Dept (6010003)', 'Resource & Development (1070006)', 'Retail Business (3010004)', 'Retail Dealing\n& Share Margin Financing Dept (6010002)', 'Retail Special Assets Management (1100009)', 'Rewards & Shared Services (1140003)', 'Risk & Compliance (1070004)', 'Risk Analytics (1210005)', 'Risk Management (3010009)', 'RO Deposit and Cash (1110008)', 'ROM & AROM (1340001)', 'Sales & Distribution (1230001)', 'Sales & Distribution Channel (1360005)', 'Sales & Marketing Strategy (3010013)', 'Sales Support (1230005)', 'Shared Services & IR (1140003)', 'Shariah (1220002)', 'Shariah Audit (1160003)', 'Shariah Business Consiltancy (1250003)', 'Shariah Centre of Excellence (1250002)', 'Shariah Compliance Department (1060005)', 'SSC Shariah (1220003)', 'SST Management (1350001)', 'Strategic Alliance (1360004)', 'Strategic Business Relations (1070012)', 'Strategic Channel & Delivery (1250003)', 'Strategic Management (1240001)', 'Strategic Management (1270002)', 'Strategic Relations (1250003)', 'Strategy & Centralized Services (1030001)', 'Strategy & Finance (1380002)', 'Strategy, Social Development & Sustainability (1250002)', 'System User Support (1390006)', 'Talent & Capabilities Development (1140006)', 'Talent Sourcing & Shared Services (1140003)', 'Technology Risk (1150001)', 'Trade Service (1020002)', 'Transaction Management (1090001)', 'Transactional Service (1090001)', 'Treasury (1270003)', 'Treasury Corp Forex Sales (1270012)', 'Treasury FX Trading (1270011)', 'Validation (1210005)', 'Valuation (1100005)', 'Value Delivery Office (1240006)', 'Vehicle Financing (1390004)'];

/*initiate the autocomplete function on the "myInput" element, and pass along the office array as possible autocomplete values:*/
autocomplete(document.getElementById("officeInput"), office);