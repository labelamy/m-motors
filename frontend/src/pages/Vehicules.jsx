import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";

function Vehicules() {
  const [vehicules, setVehicules] = useState([]);
  const [loading, setLoading] = useState(true);

  const [mesDossiers, setMesDossiers] = useState([]);

  const fetchDossiers = async () => {
  try {
    const res = await API.get("/dossiers/mes-dossiers");
    setMesDossiers(res.data);
  } catch (error) {
    console.error("Erreur dossiers :", error);
  }
};

  const navigate = useNavigate();

  const choisirVehicule = async (vehiculeId) => {
    
  try {
    const res = await API.post("/dossiers/", {
      vehicule_id: vehiculeId,
      type: "achat"
    });

    alert("Véhicule choisi ✅");
    await fetchDossiers();
    // redirection vers la page dossiers
    navigate("/dossiers");

  } catch (error) {
    console.error("Erreur création dossier", error);

     if (error.response && error.response.data?.detail) {
      alert(error.response.data.detail);
    } else {
      alert("Erreur inconnue ❌");
    }
  }
};

  const fetchVehicules = async () => {
    try {
      const res = await API.get("/vehicules/");
      setVehicules(res.data);
    } catch (error) {
      console.error("Erreur récupération véhicules :", error);
    } finally {
      setLoading(false);
    }
  };

  const vehiculeDejaChoisi = (vehiculeId) => {
  return mesDossiers.some(d => d.vehicule_id === vehiculeId);
  };

  useEffect(() => {
    fetchVehicules();
    fetchDossiers();
  }, []);

  if (loading) {
    return (
      <div className="container text-center mt-5">
        <div className="spinner-border text-primary"></div>
        <p className="mt-3">Chargement des véhicules...</p>
      </div>
    );
  }
  

  return (
    <div className="container py-5">
      <h2 className="mb-4">🚗 Véhicules Disponibles</h2>
      <div className="row g-4">
        {vehicules.length === 0 && (
          <div className="alert alert-info text-center shadow-sm">
            Aucun véhicule disponible.
          </div>
        )}

        {vehicules.map((v) => (
          <div key={v.id} className="col-12 col-md-6 col-lg-4">
            <div className="card h-100 shadow-sm border-0">

              {/* Image */}
              {v.image_url && (
                <img
                  src={v.image_url.startsWith("http") ? v.image_url : `${import.meta.env.VITE_API_URL}${v.image_url}`}
                  alt={v.model}
                  className="card-img-top img-fluid"
                  style={{ height: "220px", objectFit: "cover" }}
                  onError={(e) => {
                    e.target.src = `${import.meta.env.VITE_API_URL}/images/default_car.jpg`;
                    e.target.onerror = null;
                  }}
                />
              )}

              <div className="card-body d-flex flex-column">
                <h5 className="card-title fw-bold">
                  {v.brand} {v.model} ({v.year})
                </h5>

                <p className="mb-1">
                  <strong>Prix :</strong> {v.price.toLocaleString()} € 
                </p>

                <p className="mb-1">
                  <strong>Kilométrage :</strong> {v.kilometrage} km
                </p>

                <p className="mb-1">
                  <strong>Carburant :</strong> {v.carburant}
                </p>

                <p className="mb-1">
                  <strong>Transmission :</strong> {v.transmission}
                </p>

                <p className="mb-1">
                  <strong>Type :</strong> {v.type}
                </p>

                <p className="mb-2">
                  {v.description}
                </p>
                <div className="d-flex justify-content-between align-items-center mt-4">
                <span className={`badge badge-status ${v.available ? "bg-success" : "bg-danger"}`}>
                  {v.available ? "Disponible" : "Indisponible"}
                </span>
                {/* Bouton choisir */}
                {v.available && (
                  <button
                    className="btn btn-choose"
                    disabled={vehiculeDejaChoisi(v.id)}
                    onClick={() => choisirVehicule(v.id)}>
                     {vehiculeDejaChoisi(v.id) ? "Déjà choisi" : "🚗 Choisir"}
                  </button>)}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Vehicules;