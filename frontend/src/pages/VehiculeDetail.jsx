import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import API from "../services/api";

function VehiculeDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [vehicule, setVehicule] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isFavori, setIsFavori] = useState(false);

  const DEFAULT_IMAGE = "/seed_images/default_car.jpg";

  // 🔹 Récupérer détail véhicule
  const fetchVehicule = async () => {
  try {
    const res = await API.get(`/vehicules/${id}`);
    setVehicule(res.data);
  } catch (error) {
    console.log("Erreur véhicule :", error);
    alert("Erreur récupération véhicule ❌");
    navigate("/vehicules");
    return;
  }

  // appel séparé pour vérifier favoris (non bloquant)
  try {
    const favRes = await API.get("/favoris");
    setIsFavori(favRes.data.some(f => f.vehicule_id === Number(id)));
  } catch (error) {
    console.log("Erreur favoris :", error);
  } finally {
    setLoading(false);
  }
};

  useEffect(() => {
    console.log("ID URL:", id);
    fetchVehicule();
  }, [id]);

  if (loading) {
  return (
    <div className="container py-5 fade-in">
      <div className="row g-4">
        <div className="col-md-6">
          <div className="skeleton image"></div>
        </div>
        <div className="col-md-6">
          <div className="skeleton title"></div>
          <div className="skeleton text"></div>
          <div className="skeleton text"></div>
          <div className="skeleton text"></div>
        </div>
      </div>
      <p className="mt-3">Chargement du véhicule...</p>
    </div>
  );
}

  if (!vehicule) return null;

  const isIndisponible = !vehicule.available || vehiculeDejaChoisi(vehicule.id);

  const toggleFavori = async () => {
    try {
      if (isFavori) {
        await API.delete(`/favoris/${vehicule.id}`);
      } else {
        await API.post(`/favoris/`, { vehicule_id: vehicule.id });
      }
      setIsFavori(!isFavori);
    } catch (error) {
      console.error(error);
      alert("Erreur favoris ❌");
    }
  };

  const choisirVehicule = async () => {
    try {
      await API.post("/dossiers/", { vehicule_id: vehicule.id, type: "achat" });
      alert("Véhicule choisi ✅");
      navigate("/dossiers");
    } catch (error) {
      console.error(error);
      alert(error.response?.data?.detail || "Erreur ❌");
    }
  };

  return (
    <div className="container py-5">
      <button className="btn btn-light border mb-3" onClick={() => navigate(-1)}>
        🔙 Retour
      </button>

      <div className="row g-4">
        <div className="col-md-6">
          <img
            src={vehicule.image_url || DEFAULT_IMAGE}
            alt={vehicule.model}
            className="img-fluid rounded"
            style={{ maxHeight: "400px", objectFit: "cover" }}
            onError={(e) => { e.target.src = DEFAULT_IMAGE; }}
          />
        </div>

        <div className="col-md-6 d-flex flex-column">
          <h2>{vehicule.brand} {vehicule.model} ({vehicule.year})</h2>
          <p><strong>Prix :</strong> {vehicule.price.toLocaleString()} €</p>
          <p><strong>Kilométrage :</strong> {vehicule.kilometrage} km</p>
          <p><strong>Carburant :</strong> {vehicule.carburant}</p>
          <p><strong>Transmission :</strong> {vehicule.transmission}</p>
          <p><strong>Type :</strong> {vehicule.type}</p>
          <p><strong>Description :</strong> {vehicule.description}</p>

          <div className="mt-auto d-flex justify-content-between align-items-center">
            <button
              className={`btn ${isFavori ? "btn-danger" : "btn-outline-danger"}`}
              onClick={toggleFavori}
            >
              {isFavori ? "❤️ Favori" : "🤍 Ajouter aux favoris"}
            </button>

            {!isIndisponible && (
              <button className="btn btn-primary px-4 fw-semibold" disabled={isIndisponible} onClick={choisirVehicule}>
                {isIndisponible ? "Indisponible" : "🚗 Choisir ce véhicule"}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default VehiculeDetail;