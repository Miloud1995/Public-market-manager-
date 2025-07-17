import express from 'express';
import cors from 'cors';
import sqlite3 from 'sqlite3';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import multer from 'multer';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3001;
const JWT_SECRET = 'your-secret-key';

// Middleware
app.use(cors());
app.use(express.json());
app.use('/uploads', express.static(join(__dirname, 'uploads')));

// File upload configuration
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, join(__dirname, 'uploads'));
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + '-' + file.originalname);
  }
});
const upload = multer({ storage });

// Database setup
const db = new sqlite3.Database(':memory:');

// Initialize database tables
db.serialize(() => {
  // Users table for authentication
  db.run(`
    CREATE TABLE users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      email TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL,
      role TEXT DEFAULT 'user',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Maître d'ouvrage (Project Owner)
  db.run(`
    CREATE TABLE maitre_ouvrage (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nom TEXT NOT NULL,
      adresse TEXT,
      telephone TEXT,
      email TEXT,
      responsable TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Prestataire (Service Provider)
  db.run(`
    CREATE TABLE prestataire (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nom TEXT NOT NULL,
      adresse TEXT,
      telephone TEXT,
      email TEXT,
      specialite TEXT,
      numero_registre TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Marché (Market/Contract)
  db.run(`
    CREATE TABLE marche (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      numero TEXT UNIQUE NOT NULL,
      objet TEXT NOT NULL,
      type TEXT NOT NULL,
      montant REAL NOT NULL,
      date_signature DATE,
      date_debut DATE,
      date_fin DATE,
      statut TEXT DEFAULT 'en_cours',
      maitre_ouvrage_id INTEGER,
      prestataire_id INTEGER,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (maitre_ouvrage_id) REFERENCES maitre_ouvrage(id),
      FOREIGN KEY (prestataire_id) REFERENCES prestataire(id)
    )
  `);

  // Service
  db.run(`
    CREATE TABLE service (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      libelle TEXT NOT NULL,
      description TEXT,
      prix_unitaire REAL,
      unite TEXT,
      marche_id INTEGER,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (marche_id) REFERENCES marche(id)
    )
  `);

  // Maintenance
  db.run(`
    CREATE TABLE maintenance (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      libelle TEXT NOT NULL,
      description TEXT,
      prix_unitaire REAL,
      periodicite TEXT,
      marche_id INTEGER,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (marche_id) REFERENCES marche(id)
    )
  `);

  // Fourniture (Supply)
  db.run(`
    CREATE TABLE fourniture (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      libelle TEXT NOT NULL,
      description TEXT,
      prix_unitaire REAL,
      unite TEXT,
      marque TEXT,
      marche_id INTEGER,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (marche_id) REFERENCES marche(id)
    )
  `);

  // Ordre de service
  db.run(`
    CREATE TABLE ordre_service (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      numero TEXT UNIQUE NOT NULL,
      objet TEXT NOT NULL,
      date_emission DATE,
      date_execution DATE,
      statut TEXT DEFAULT 'en_attente',
      marche_id INTEGER,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (marche_id) REFERENCES marche(id)
    )
  `);

  // Décompte
  db.run(`
    CREATE TABLE decompte (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      numero TEXT UNIQUE NOT NULL,
      periode_debut DATE,
      periode_fin DATE,
      montant_ht REAL,
      montant_ttc REAL,
      statut TEXT DEFAULT 'brouillon',
      marche_id INTEGER,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (marche_id) REFERENCES marche(id)
    )
  `);

  // PV (Procès-verbal)
  db.run(`
    CREATE TABLE pv (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      numero TEXT UNIQUE NOT NULL,
      type TEXT NOT NULL,
      date_pv DATE,
      objet TEXT,
      observations TEXT,
      marche_id INTEGER,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (marche_id) REFERENCES marche(id)
    )
  `);

  // Document
  db.run(`
    CREATE TABLE document (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nom TEXT NOT NULL,
      type TEXT,
      chemin TEXT,
      taille INTEGER,
      marche_id INTEGER,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (marche_id) REFERENCES marche(id)
    )
  `);

  // Insert sample data
  const password = bcrypt.hashSync('admin123', 8);
  db.run('INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)', 
    ['admin', 'admin@example.com', password, 'admin']);

  // Sample data
  db.run(`INSERT INTO maitre_ouvrage (nom, adresse, telephone, email, responsable) VALUES 
    ('Ministère des Travaux Publics', '123 Rue de la République', '01234567', 'contact@mtp.gov', 'Jean Dupont'),
    ('Mairie de Paris', '5 Place de l\'Hôtel de Ville', '01234568', 'contact@paris.fr', 'Marie Martin')`);

  db.run(`INSERT INTO prestataire (nom, adresse, telephone, email, specialite, numero_registre) VALUES 
    ('BTP Construction', '456 Avenue des Bâtisseurs', '01234569', 'contact@btp.com', 'Construction', 'RC123456'),
    ('Services Maintenance', '789 Rue de la Maintenance', '01234570', 'info@maintenance.com', 'Maintenance', 'RC789012')`);

  db.run(`INSERT INTO marche (numero, objet, type, montant, date_signature, date_debut, date_fin, statut, maitre_ouvrage_id, prestataire_id) VALUES 
    ('M2024001', 'Construction d\'un pont', 'Travaux', 500000.00, '2024-01-15', '2024-02-01', '2024-12-31', 'en_cours', 1, 1),
    ('M2024002', 'Maintenance des routes', 'Maintenance', 150000.00, '2024-01-20', '2024-02-01', '2024-12-31', 'en_cours', 2, 2)`);
});

// Authentication middleware
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Token d\'accès requis' });
  }

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Token invalide' });
    }
    req.user = user;
    next();
  });
};

// Auth routes
app.post('/api/auth/login', (req, res) => {
  const { email, password } = req.body;
  
  db.get('SELECT * FROM users WHERE email = ?', [email], (err, user) => {
    if (err) {
      return res.status(500).json({ error: 'Erreur serveur' });
    }
    
    if (!user || !bcrypt.compareSync(password, user.password)) {
      return res.status(401).json({ error: 'Identifiants invalides' });
    }
    
    const token = jwt.sign(
      { id: user.id, email: user.email, role: user.role },
      JWT_SECRET,
      { expiresIn: '24h' }
    );
    
    res.json({
      token,
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        role: user.role
      }
    });
  });
});

// Generic CRUD routes generator
const createCrudRoutes = (tableName, primaryKey = 'id') => {
  // GET all
  app.get(`/api/${tableName}`, authenticateToken, (req, res) => {
    const { page = 1, limit = 10, search = '' } = req.query;
    const offset = (page - 1) * limit;
    
    let query = `SELECT * FROM ${tableName}`;
    let countQuery = `SELECT COUNT(*) as total FROM ${tableName}`;
    const params = [];
    
    if (search) {
      query += ` WHERE nom LIKE ? OR libelle LIKE ? OR numero LIKE ? OR objet LIKE ?`;
      countQuery += ` WHERE nom LIKE ? OR libelle LIKE ? OR numero LIKE ? OR objet LIKE ?`;
      const searchParam = `%${search}%`;
      params.push(searchParam, searchParam, searchParam, searchParam);
    }
    
    query += ` ORDER BY ${primaryKey} DESC LIMIT ? OFFSET ?`;
    params.push(parseInt(limit), offset);
    
    db.get(countQuery, search ? params.slice(0, 4) : [], (err, countResult) => {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      
      db.all(query, params, (err, rows) => {
        if (err) {
          return res.status(500).json({ error: err.message });
        }
        
        res.json({
          data: rows,
          total: countResult.total,
          page: parseInt(page),
          totalPages: Math.ceil(countResult.total / limit)
        });
      });
    });
  });

  // GET by ID
  app.get(`/api/${tableName}/:id`, authenticateToken, (req, res) => {
    db.get(`SELECT * FROM ${tableName} WHERE ${primaryKey} = ?`, [req.params.id], (err, row) => {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      if (!row) {
        return res.status(404).json({ error: 'Enregistrement non trouvé' });
      }
      res.json(row);
    });
  });

  // POST create
  app.post(`/api/${tableName}`, authenticateToken, (req, res) => {
    const data = req.body;
    const keys = Object.keys(data);
    const values = Object.values(data);
    const placeholders = keys.map(() => '?').join(', ');
    
    const query = `INSERT INTO ${tableName} (${keys.join(', ')}) VALUES (${placeholders})`;
    
    db.run(query, values, function(err) {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      res.json({ id: this.lastID, message: 'Enregistrement créé avec succès' });
    });
  });

  // PUT update
  app.put(`/api/${tableName}/:id`, authenticateToken, (req, res) => {
    const data = req.body;
    const keys = Object.keys(data);
    const values = Object.values(data);
    const setClause = keys.map(key => `${key} = ?`).join(', ');
    
    const query = `UPDATE ${tableName} SET ${setClause}, updated_at = CURRENT_TIMESTAMP WHERE ${primaryKey} = ?`;
    values.push(req.params.id);
    
    db.run(query, values, function(err) {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      if (this.changes === 0) {
        return res.status(404).json({ error: 'Enregistrement non trouvé' });
      }
      res.json({ message: 'Enregistrement mis à jour avec succès' });
    });
  });

  // DELETE
  app.delete(`/api/${tableName}/:id`, authenticateToken, (req, res) => {
    db.run(`DELETE FROM ${tableName} WHERE ${primaryKey} = ?`, [req.params.id], function(err) {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      if (this.changes === 0) {
        return res.status(404).json({ error: 'Enregistrement non trouvé' });
      }
      res.json({ message: 'Enregistrement supprimé avec succès' });
    });
  });
};

// Create CRUD routes for all tables
const tables = [
  'maitre_ouvrage', 'prestataire', 'marche', 'service', 
  'maintenance', 'fourniture', 'ordre_service', 'decompte', 'pv', 'document'
];

tables.forEach(table => createCrudRoutes(table));

// Special routes for relationships
app.get('/api/marche/:id/services', authenticateToken, (req, res) => {
  db.all('SELECT * FROM service WHERE marche_id = ?', [req.params.id], (err, rows) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json(rows);
  });
});

app.get('/api/marche/:id/maintenances', authenticateToken, (req, res) => {
  db.all('SELECT * FROM maintenance WHERE marche_id = ?', [req.params.id], (err, rows) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json(rows);
  });
});

app.get('/api/marche/:id/fournitures', authenticateToken, (req, res) => {
  db.all('SELECT * FROM fourniture WHERE marche_id = ?', [req.params.id], (err, rows) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json(rows);
  });
});

// Dashboard statistics
app.get('/api/dashboard/stats', authenticateToken, (req, res) => {
  const stats = {};
  
  const queries = [
    { key: 'totalMarches', query: 'SELECT COUNT(*) as count FROM marche' },
    { key: 'totalPrestataires', query: 'SELECT COUNT(*) as count FROM prestataire' },
    { key: 'totalMaitreOuvrage', query: 'SELECT COUNT(*) as count FROM maitre_ouvrage' },
    { key: 'totalDocuments', query: 'SELECT COUNT(*) as count FROM document' },
    { key: 'marchesEnCours', query: 'SELECT COUNT(*) as count FROM marche WHERE statut = "en_cours"' },
    { key: 'montantTotal', query: 'SELECT SUM(montant) as sum FROM marche' }
  ];
  
  let completed = 0;
  
  queries.forEach(({ key, query }) => {
    db.get(query, (err, result) => {
      if (!err) {
        stats[key] = result.count || result.sum || 0;
      }
      completed++;
      if (completed === queries.length) {
        res.json(stats);
      }
    });
  });
});

// File upload
app.post('/api/upload', authenticateToken, upload.single('file'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'Aucun fichier fourni' });
  }
  
  res.json({
    filename: req.file.filename,
    originalname: req.file.originalname,
    size: req.file.size,
    path: `/uploads/${req.file.filename}`
  });
});

app.listen(PORT, () => {
  console.log(`Serveur démarré sur le port ${PORT}`);
});