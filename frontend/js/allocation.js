let scientists = [
    { name:"Dr. Srinivasan", specialization:"artificial intelligence", assigned:[] },
    { name:"Dr. Ananya Mehta", specialization:"cybersecurity", assigned:[] },
    { name:"Dr. Vivek Sharma", specialization:"machine learning", assigned:[] },
    { name:"Dr. Priya Nair", specialization:"computer vision", assigned:[] }
];

let interns = [
    { name:"Rahul", skills:"machine learning", selected:true },
    { name:"Simran", skills:"artificial intelligence", selected:true },
    { name:"Aman", skills:"cybersecurity", selected:true }
];

function allocate(){
    scientists.forEach(s=>s.assigned=[]);

    interns.forEach(i=>{
        if(!i.selected) return;

        let sk=i.skills.toLowerCase();

        for(let s of scientists){
            if(sk.includes(s.specialization)){
                s.assigned.push(i.name);
                i.allotted=s.name;
                break;
            }
        }
    });
}

function render(){

    allocate();

    let q=document.getElementById("search").value?.toLowerCase() || "";

    const container=document.getElementById("container");
    container.innerHTML="";

    scientists
    .filter(s=>s.name.toLowerCase().includes(q))
    .forEach(s=>{

        container.innerHTML+=`
        <div class="card">

            <h3>${s.name}</h3>

            <div class="badge">${s.specialization}</div>

            <p>Assigned: ${s.assigned.length}</p>

            <h4>Interns</h4>

            <ul>
                ${s.assigned.length
                    ? s.assigned.map(i=>`<li>${i}</li>`).join("")
                    : "<li>No interns assigned</li>"
                }
            </ul>

        </div>
        `;
    });
}

function openScientist(){
    document.getElementById("scientistModal").style.display="flex";
}

function openIntern(){
    document.getElementById("internModal").style.display="flex";
}

function closeModal(){
    document.querySelectorAll(".modal").forEach(m=>m.style.display="none");
}

function addScientist(){
    scientists.push({
        name:sName.value,
        specialization:sSpec.value,
        assigned:[]
    });

    closeModal();
    render();
}

function addIntern(){
    interns.push({
        name:iName.value,
        skills:iSkills.value,
        selected:true
    });

    closeModal();
    render();
}

function load(){
    render();
}

load();