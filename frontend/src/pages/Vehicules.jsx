import { useEffect, useState } from "react";
import API from "../services/api";

function Vehicles() {
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchVehicles = async () => {
      try {
        const response = await API.get("/vehicules/");
        setVehicles(response.data);
      } catch (error) {
        console.error("Erreur lors de la récupération des véhicules :", error);
      } finally {
        setLoading(false);
      }
    };

    fetchVehicles();
  }, []);

  if (loading) {
    return <p>Chargement des véhicules...</p>;
  }

  return (
    <div className="container mt-5">
      <h2>Liste des véhicules</h2>
      {vehicles.length === 0 ? (
        <p>Aucun véhicule disponible.</p>
      ) : (
        <div className="row">
          {vehicles.map((v) => (
            <div key={v.id} className="col-md-4 mb-3">
              <div className="card">
                <div className="card-body">
                  <h5 className="card-title">{v.brand} {v.model}</h5>
                  <p className="card-text">Type : {v.type}</p>
                  <p className="card-text">Prix : {v.price} €</p>
                  <p className="card-text">
                    {v.available ? "Disponible" : "Indisponible"}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Vehicles;