const featureConfigs = {
  "routes": {
    title: "🚛 Projet ROUTES",
    description: "Veuillez uploader les fichiers nécessaires pour analyser les routes.",
    endpoint: "routes",
    inputs: {
      "trucks_file": "AVAILABLE_TRUCKS",
      "invoice_file": "INVOICE_WITH_GEO_LOCATION"
    }
  },
  "po-vs-commande": {
    title: "📋 PO vs Commande",
    description: "Comparer les bons de commande avec les commandes fournisseurs.",
    endpoint: "po-vs-commande",
    inputs: {
      "po_file": "Bon de commande (PO)",
      "supplier_file": "Commande fournisseur"
    }
  },
  "achat-vs-invoice": {
    title: "📦 Achat vs Invoice vs Packing",
    description: "Contrôle croisé entre achat, facture et packing list.",
    endpoint: "achat-vs-invoice",
    inputs: {
      "achat_file": "Bon d'achat",
      "invoice_file": "Facture",
      "packing_file": "Packing list"
    }
  },
  "po-vs-pi": {
    title: "📊 PO vs PI",
    description: "Comparer PO et PI pour cohérence.",
    endpoint: "po-vs-pi",
    inputs: {
      "po_file": "Bon de commande (PO)",
      "pi_file": "Proforma Invoice"
    }
  },
  "po-vs-mtc": {
    title: "⚡ PO vs MTC",
    description: "Analyse automatique des documents PO et MTC.",
    endpoint: "po-vs-mtc",
    inputs: {
      "po_file": "PO",
      "mtc_file": "MTC"
    }
  },
  "logistics": {
    title: "🌍 Logistique",
    description: "Envoyez le fichier logistique à analyser.",
    endpoint: "logistics",
    inputs: {
      "logistics_file": "Fichier logistique"
    }
  },
  "option7": {
    title: "🔢 Option 7",
    description: "Fonctionnalité personnalisée.",
    endpoint: "option7",
    inputs: {
      "file": "Fichier"
    }
  },
  "option8": {
    title: "🔢 Option 8",
    description: "Fonctionnalité personnalisée.",
    endpoint: "option8",
    inputs: {
      "file": "Fichier"
    }
  },
  "option9": {
    title: "🔢 Option 9",
    description: "Fonctionnalité personnalisée.",
    endpoint: "option9",
    inputs: {
      "file": "Fichier"
    }
  }
};

let selectedFeature = null;

function openModal(featureKey) {
  selectedFeature = featureKey;
  const config = featureConfigs[featureKey];

  document.getElementById("modal-title").textContent = config.title;
  document.getElementById("modal-description").textContent = config.description;

  const inputsContainer = document.getElementById("file-inputs");
  inputsContainer.innerHTML = "";

  for (const [name, label] of Object.entries(config.inputs)) {
    const wrapper = document.createElement("div");
    wrapper.classList.add("input-wrapper");

    const labelEl = document.createElement("label");
    labelEl.textContent = `📎 ${label}`;
    labelEl.setAttribute("for", name);

    const inputEl = document.createElement("input");
    inputEl.type = "file";
    inputEl.id = name;
    inputEl.name = name;

    wrapper.appendChild(labelEl);
    wrapper.appendChild(inputEl);
    inputsContainer.appendChild(wrapper);
  }

  document.getElementById("modal").style.display = "block";
}

function closeModal() {
  document.getElementById("modal").style.display = "none";
  document.getElementById("file-inputs").innerHTML = "";
}

// ✅ Called by "Envoyer" button (onclick="onSendButtonClick(event)")
function onSendButtonClick(event) {
  event.preventDefault();

  const config = featureConfigs[selectedFeature];
  const formData = new FormData();

  for (const name of Object.keys(config.inputs)) {
    const file = document.getElementById(name)?.files[0];
    if (!file) {
      alert(`❌ Fichier requis : ${config.inputs[name]}`);
      return;
    }
    formData.append(name, file);
  }

  // ✅ Open new tab BEFORE any async calls
  const resultWindow = window.open('result.html', '_blank');
  if (!resultWindow) {
    alert("❌ Le navigateur a bloqué la fenêtre. Veuillez autoriser les popups.");
    return;
  }

  // ✅ Proceed to upload and fetch result
  fetch(`http://localhost:8000/analyze/${config.endpoint}`, {
    method: "POST",
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      if (data.result) {
        resultWindow.postMessage({
          type: 'analysis_result',
          payload: data.result
        }, '*');
        closeModal();
      } else {
        resultWindow.postMessage({
          type: 'analysis_result',
          payload: `<h2>❌ Erreur de traitement</h2><p>${data.error || "Analyse échouée."}</p>`
        }, '*');
      }
    })
    .catch(err => {
      resultWindow.postMessage({
        type: 'analysis_result',
        payload: `<h2>❌ Erreur réseau</h2><p>${err.message}</p>`
      }, '*');
    });
}
