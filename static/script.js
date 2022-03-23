// api url
const api_url =
    "http://127.0.0.1:5000/getData";

async function getapi(url) {

    const response = await fetch(url);

    var data = await response.json();
    show(data);
}
getapi(api_url);

function show(data) {
    let tab =
        `<tr class="row header">
		<th class="cell">S. No.</th>
		<th class="cell">BloodBank Id</th>
		<th class="cell">Employee Id</th>
		<th class="cell">No. of Blood Bags available (A+)</th>
		<th class="cell">No. of Blood Bags available (A-)</th>
		<th class="cell">No. of Blood Bags available (B+)</th>
		<th class="cell">No. of Blood Bags available (B-)</th>
		<th class="cell">No. of Blood Bags available (AB+)</th>
		<th class="cell">No. of Blood Bags available (AB-)</th>
		<th class="cell">No. of Blood Bags available (O+)</th>
		<th class="cell">No. of Blood Bags available (O-)</th>
		</tr>`;

    for (var i = 0; i < Object.keys(data).length; i++) {
        tab += `<tr class="row">
	<td class="cell">${i + 1} </td>
	<td class="cell">${data[i].BloodBankId} </td>
	<td class="cell">${data[i].EmployeeId}</td>
	<td class="cell">${data[i].Type_APos}</td>
	<td class="cell">${data[i].Type_ANeg}</td>		
	<td class="cell">${data[i].Type_BPos}</td>
	<td class="cell">${data[i].Type_BNeg}</td>		
	<td class="cell">${data[i].Type_ABPos}</td>
	<td class="cell">${data[i].Type_ABNeg}</td>		
	<td class="cell">${data[i].Type_OPos}</td>
	<td class="cell">${data[i].Type_ONeg}</td>		
</tr>`;
    }
    document.getElementById("BloodBankTable").innerHTML = tab;
}
