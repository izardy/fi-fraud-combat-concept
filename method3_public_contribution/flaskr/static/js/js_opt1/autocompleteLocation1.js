var state = ['JOHOR',
 'PULAU PINANG',
 'KEDAH',
 'KELANTAN',
 'MELAKA',
 'NEGERI SEMBILAN',
 'PAHANG',
 'PERAK',
 'PERLIS',
 'SABAH',
 'SARAWAK',
 'SELANGOR',
 'TERENGGANU',
 'W.P. KUALA LUMPUR',
 'W.P. LABUAN',
 'W.P. PUTRAJAYA'];
var stateSelect = document.getElementById("stateSelect");
state.forEach(function(stateName) {
  var option = document.createElement("option");
  option.text = stateName;
  stateSelect.add(option);
});