# 01 — High-Detail Roman Colosseum Architecture Specification (Concept 02)

## 1. Executive Summary & Architectural Overhaul Overview

**Concept 02 (`SM_ArenaEnvironment_Colosseum_01`)** is a complete ground-up architectural reconstruction of the surrounding Roman Colosseum environment for **Map 01 — Main Arena (*Sphere Brawl: Rolling Rampage*)**. Whereas Concept 01 (`8,952` triangles) functioned as a coarse blockout shell with flat slabs and unarticulated arches, **Concept 02 delivers `186,588` instantiated triangles (`559,764` vertices) across 40 radial amphitheater bays — a `20.84×` increase in real 3D architectural geometry** — while organizing the geometry into **5 unique modular archetypes totaling `19,428` triangles** so every single module imports cleanly under Roblox Studio's `20,000`-triangle per-mesh limit.

Every architectural feature that defines a monumental Flavian Roman amphitheater is modeled in physical 3D geometry rather than painted onto flat textures:

| Architectural System | Concept 01 (Blockout) | Concept 02 (High-Detail Roman Colosseum) | Named Submesh(es) | Instantiated Triangles |
| :--- | :--- | :--- | :--- | ---: |
| **1. Exterior Classical Arcade & Arches** | Flat 1-ring polygonal openings, no soffit vaults or archivolts | 3 tiered stories of arched arcades (`120` arches total), 9/7/13 wedge voussoirs per arch, projecting keystones (`s = 1.07`), moulded imposts, dual concentric archivolts, and `6.0`-stud deep radial barrel-vaulted soffits | `COL_ExteriorArcade` | `34,880` |
| **2. Classical Column Orders (L1–L3)** | Simple unprofiled cylinders without capitals or bases | **Level 1 Tuscan/Doric** (smooth entasis shafts + echinus/abacus), **Level 2 Fluted Ionic** (12-facet fluted shafts + twin 3D coiled spiral volutes), **Level 3 Fluted Corinthian** (12-facet fluted shafts + 2 staggered tiers of 3D projecting acanthus leaves + abacus fleuron boss) | `COL_ColumnOrders` | `30,640` |
| **3. Beveled Ashlar Travertine Masonry** | Smooth continuous cylinders with no block courses or joints | Individually beveled Roman *opus quadratum* ashlar stone blocks with `0.06..0.10`-stud V-groove mortar channels (`MAT_BasaltShadow`) and deterministic 3-tone travertine block color variation | `COL_StoneMasonry` | `36,608` |
| **4. Multi-Tiered Elliptical Seating Bowl (*Cavea*)** | 6 coarse unprofiled steps, no walkways or stairs | **22 distinct profiled seating tiers** across *Ima Cavea* (8 marble tiers), *Media Cavea* (8 travertine tiers), and *Summa Cavea* (6 upper tiers) with bullnose treads, recessed risers, stone benches, 3 *praecinctiones* walkways, and 16 radial *scalaria* staircases | `COL_CaveaSeating` | `30,080` |
| **5. Vaulted *Vomitoria* & *Podium* Entrances** | Simple rectangular holes | **8 vaulted *vomitoria* portals** interrupting the *Media Cavea* with 7-voussoir stone arches, projecting keystones, flanked by moulded stone jambs and dark-neutral vaulted tunnels | `COL_Vomitoria` | `9,760` |
| **6. Fourth-Level Attic, *Clipei* & *Velarium* Rig** | Flat upper ring wall | Fluted Composite/Corinthian pilasters, alternating recessed framed attic windows and **3D circular bronze *clipei* shields** (`MAT_BronzeClipeus`), **80 projecting travertine corbel brackets**, and **40 vertical *velarium* masts** (`Y = 109.2..118.2`) | `COL_AtticCornice` | `22,320` |
| **7. Cardinal Triumphal Gate Pavilions (N/E/S/W)** | Basic boxy corner/cardinal blocks | **4 monumental Roman Triumphal Arch gate pavilions** with 13-voussoir arches, paired freestanding Corinthian columns on tall pedestals, flanking niche bays, inscribed dedicatory attic panels, and triangular classical pediments (`Y = 114.6..121.0`) | `COL_GateTowers` | `20,496` |
| **8. North Imperial *Pulvinar* / Reactor Tribune** | Small cyan strip on north rim | **North (`-Z`) Imperial Tribune & Reactor Crest** (`Y = 114.6..125.0`) with twin Corinthian aedicula columns, bronze imperial eagle/wreath standard, and disciplined cyan/amber energy core (`0.24%` total surface area) | `COL_NorthReactorCrest` | `1,804` |
| **Total High-Detail Amphitheater** | **`8,952` tris** | **`186,588` instantiated tris (`19,428` unique modular tris — `20.84×` Concept 01)** | **8 Submesh Groups** | **`186,588`** |

---

## 2. Detailed Specification of the 7 Architectural Systems

### 2.1 Four-Story Classical Exterior Facade & Column Orders (`COL_ExteriorArcade` + `COL_ColumnOrders`)
The outer elliptical facade (`R_outer_x = 128.0` studs, `R_outer_z = 134.0` studs) rises across four classical Roman stories above a stepped 2-tier travertine *crepidine* base (`Y = 48.0..51.0` studs) and a rusticated volcanic tuff foundation (`Y = 18.06..48.0` studs):

1. **Story 1 — Lower Arcade (`Y = 51.0..67.6` studs, Tuscan / Doric Order)**:
   - **Piers & Arches**: Heavy ashlar travertine piers (`R = 123.5..128.0`) framing semicircular arched openings (`Y_spring = 58.2`, `R_arch = 4.2` studs) with 9 wedge voussoirs, projecting central keystone, and moulded impost caps.
   - **Tuscan / Doric Engaged Columns**: Mounted on square travertine pedestals (`Y = 51.0..53.2`) with moulded Attic bases (`Y = 53.2..54.0`), 10-sided smooth entasis shafts (`Y = 54.0..64.3`), astragal necking rings, flared echinus cushions, and square beveled abaci (`Y = 64.3..65.6`).
   - **First Entablature (`Y = 65.6..67.6` studs)**: Layered 3D architrave, Doric frieze with projecting triglyph blocks, and overhanging cornice slab.

2. **Story 2 — Middle Arcade (`Y = 67.6..83.6` studs, Ionic Order)**:
   - **Arched Gallery & Balustrade**: 9-voussoir semicircular arches (`Y_spring = 74.6`, `R_arch = 4.0` studs) with marble parapet balustrades (`Y = 67.6..69.5`) featuring 5 stone balusters and a moulded top rail inside each arch opening.
   - **Fluted Ionic Engaged Columns**: Mounted on pedestals (`Y = 67.6..69.6`) with stepped torus-scotia-torus Attic bases (`Y = 69.6..70.3`), 12-facet vertically fluted travertine shafts (`Y = 70.3..80.1`), and **sculpted 3D Ionic capitals (`Y = 80.1..81.6`)** featuring an echinus cushion, twin projecting 3D octagonal spiral volute bolsters (`MAT_ImperialMarble`), and raised bronze spiral eyes (`MAT_BronzeClipeus`).
   - **Second Entablature (`Y = 81.6..83.6` studs)**: Stepped architrave, frieze band with recessed shadow channel, 3D dentil block course, and projecting corona cornice.

3. **Story 3 — Upper Arcade (`Y = 83.6..98.8` studs, Corinthian Order)**:
   - **Arched Gallery & Spandrel Medallions**: 7-voussoir semicircular arches (`Y_spring = 90.2`, `R_arch = 3.8` studs) with marble balustrades and twin 3D bronze spandrel medallions above the arch haunches.
   - **Fluted Corinthian Engaged Columns**: Mounted on pedestals (`Y = 83.6..85.5`) with Attic bases (`Y = 85.5..86.2`), 12-facet vertically fluted shafts (`Y = 86.2..94.8`), and **multi-tiered 3D Corinthian capitals (`Y = 94.8..96.8`)** featuring an inner bell (*calathus*), **two staggered tiers of 8 projecting 3D acanthus leaves** (`4` lower + `4` upper diagonal leaves), and a profiled abacus crowned with a bronze fleuron boss.
   - **Third Entablature (`Y = 96.8..98.8` studs)**: Layered architrave, frieze, dentil course, and deep projecting cornice.

4. **Story 4 — Attic Story & Crowning Cornice (`Y = 98.8..114.6` studs, Composite / Corinthian Pilasters)**:
   - Divided into 3 horizontal ashlar bands separated by projecting stringcourses, articulated at every bay boundary by a **fluted Composite/Corinthian pilaster** (`3` vertical flute channels, Attic base, and 3D acanthus capital).
   - **Alternating Attic Bays**: Even bays feature **recessed rectangular Roman windows** (`Y = 102.8..108.2`) with projecting marble sills, moulded jambs, and lintel hoods; odd bays feature **3D sculpted circular bronze *clipei* shields** (`R = 2.4` studs, `MAT_BronzeClipeus`) with raised marble umbilical bosses (`MAT_ImperialMarble`).
   - **Corbel Brackets & *Velarium* Masts**: Every bay carries **2 projecting travertine corbel brackets** (`80` total) at `Y = 108.6..111.4` and a **vertical bronze-sheathed *velarium* mast** (`40` total, `Y = 109.2..118.2`) passing through the crowning dentil-and-corona cornice (`Y = 111.8..114.6`).

---

### 2.2 Multi-Tiered Elliptical Seating Bowl (*Cavea*), *Praecinctiones*, *Scalaria* & *Vomitoria* (`COL_CaveaSeating` + `COL_Vomitoria`)
The interior seating bowl spans from the inner elliptical arena wall (`R_inner = 98.0 × 104.0` studs) outward to the upper colonnade gallery (`R = 123.5 × 129.5` studs), rising from `Y = 53.2` to `Y = 98.8` studs:

- **Podium Wall & Senatorial *Balteus* (`R = 98.0..101.2`, `Y = 44.0..55.4`)**:
  - Rusticated lower podium wall dropping into the sub-arena void, topped by a projecting marble *podium* cornice (`Y = 52.0..53.2`), senatorial box walkway, and panelled marble parapet (`Y = 53.2..55.4`) with carved relief panels and square terminal posts.
- **22 Profiled Stone Seating Tiers**:
  - **Tier 1 — *Ima Cavea* (Senatorial & Equestrian Lower Bowl, `8` marble steps, `R = 101.2..108.4`, `Y = 53.8..64.2`)**: Each step is individually modeled with a recessed vertical riser, a projecting `0.14`-stud bullnose nosing (`MAT_ImperialMarble`), and a wide stone bench tread.
  - **First *Praecinctio* (`R = 108.4..110.2`, `Y = 64.2..67.2`)**: Horizontal concentric circulation walkway backed by a `3.0`-stud *balteus* parapet wall with moulded marble coping.
  - **Tier 2 — *Media Cavea* (Main Citizen Middle Bowl, `8` travertine steps, `R = 110.2..117.4`, `Y = 66.2..78.2`)**: 8 profiled travertine seating tiers with projecting bullnose nosings and recessed risers.
  - **Second *Praecinctio* (`R = 117.4..119.0`, `Y = 78.2..81.4`)**: Second horizontal walkway and moulded *balteus* parapet wall.
  - **Tier 3 — *Summa Cavea* (Upper Steep Bowl & Colonnade Gallery, `6` steps, `R = 119.0..123.5`, `Y = 80.6..90.8`)**: 6 steeper upper seating tiers crowned by the *Porticus in Summa Cavea* (`Y = 90.8..98.8`) with interior columns and balustered parapet overlooking the arena.
- **16 Radial *Scalaria* Staircases**:
  - Placed around all 4 quadrants between the cardinal gates and *vomitoria*, cutting radially up the *Ima* and *Media Cavea* with **double-density stepped stone treads** (`16` sub-steps per tier) and **stepped stone stringer handrails** (`MAT_ImperialMarble`).
- **8 Vaulted *Vomitoria* Entrance Portals (`COL_Vomitoria`)**:
  - Located at symmetric inter-cardinal bays (`b = 3, 7, 13, 17, 23, 27, 33, 37`), cutting into the *Media Cavea* (`R = 110.2..118.5`, `Y = 64.2..77.0`) with **7-voussoir stone arches**, projecting marble keystones, heavy side parapet walls, and deep dark-neutral vaulted exit tunnels (`MAT_DarkNeutral`).

---

### 2.3 Four Cardinal Triumphal Gate Pavilions & North Imperial Tribune (`COL_GateTowers` + `COL_NorthReactorCrest`)
At the four cardinal compass points — **North (`-Z`, Bay 30)**, **East (`+X`, Bay 0)**, **South (`+Z`, Bay 10)**, and **West (`-X`, Bay 20)** — the amphitheater is anchored by monumental projecting **Roman Triumphal Arch Gate Pavilions**:
- **Twin Projecting Ashlar Pylons** extending from the inner *podium* (`R = 98.0`) to `R = 130.0 × 136.0` studs (`2.0` studs proud of the standard outer arcade).
- **13-Voussoir Monumental Central Arch (`Y = 51.0..84.0`)** with a massive projecting marble keystone (`s = 1.12`), deep coffered barrel-vaulted passageway, and dark-neutral portal throat (`MAT_DarkNeutral`).
- **Paired Freestanding Corinthian Columns** flanking both the arena-facing and exterior-facing facades on tall panelled pedestals (`Y = 51.0..56.5`), with 12-flute shafts (`Y = 56.5..79.5`) and sculpted 3D Corinthian acanthus capitals (`Y = 79.5..82.5`).
- **Classical Pediment & Dedicatory Attic (`Y = 84.0..121.0`)**: Moulded entablature with dentil frieze, inscribed dedicatory attic story (`Y = 87.5..114.6`) flanked by twin bronze *clipei* shields, and a **crowned triangular Roman pediment (`Y = 114.6..121.0`)** with raking cornices and recessed tympanum.
- **North (`-Z`) Imperial *Pulvinar* / Reactor Crest (`COL_NorthReactorCrest`, `Y = 114.6..125.0`)**: Exclusively crowns the North (`-Z`) gate pavilion with an elevated Imperial Tribune aedicula, twin Corinthian columns, imperial bronze eagle/wreath standard, and a central recessed cyan/amber energy core (`EMI_Cyan` + `EMI_Amber`), providing instant visual compass orientation from the elevated gameplay camera.

---

## 3. Material & Lighting Palette Breakdown

All surface areas across the `186,588` triangles have been measured in square studs to verify strict compliance with the warm Roman stone material budget and the `<= 8%` emissive cap:

| Material Slot | Architectural Role | Base RGB | Roughness / Metalness | Surface Area (sq studs) | Area Share (%) |
| :--- | :--- | :---: | :---: | ---: | ---: |
| `MAT_TravertineWarm` | Main pier shafts, ashlar blocks (tone A), upper seating treads, attic walls | `(206, 189, 162)` | `0.78 / 0.00` | `356,678.31` | `45.22%` |
| `MAT_TravertineLight` | Engaged columns, arch voussoirs, entablature architraves, corbels | `(224, 210, 186)` | `0.72 / 0.00` | `177,909.13` | `22.56%` |
| `MAT_TuffFoundation` | Lower rusticated foundation blocks, *cavea* risers, inner vault ribs | `(138, 124, 108)` | `0.88 / 0.00` | `122,605.49` | `15.55%` |
| `MAT_ImperialMarble` | Sculpted capitals (Tuscan/Ionic/Corinthian), keystones, *Ima Cavea* treads, cornices | `(238, 232, 220)` | `0.55 / 0.00` | `77,933.74` | `9.88%` |
| `MAT_BasaltShadow` | Ashlar V-groove mortar channels, deep barrel vault soffits, shadow reveals | `(58, 55, 52)` | `0.90 / 0.00` | `25,700.19` | `3.26%` |
| `MAT_LimestoneCream` | Ashlar highlight blocks, balustrade rails, dedicatory tablets | `(232, 221, 200)` | `0.68 / 0.00` | `21,312.77` | `2.70%` |
| `MAT_DarkNeutral` | *Vomitoria* tunnel interiors, attic window openings, gate portal throats | `(24, 26, 32)` | `0.95 / 0.00` | `3,713.36` | `0.47%` |
| `MAT_BronzeClipeus` | Attic *clipei* shields, *velarium* masts, spandrel bosses, imperial standard | `(168, 132, 74)` | `0.38 / 0.82` | `983.69` | `0.12%` |
| `EMI_Cyan` | Subtle sub-cornice architectural accent strip & North Imperial Tribune core | `(0, 240, 255)` | `Emissive` | `1,853.53` | `0.24%` |
| `EMI_Amber` | North Imperial Tribune upper beacon pip | `(255, 155, 25)` | `Emissive` | `8.12` | `< 0.01%` |
| **Total** | **99.76% Authentic Roman Stone/Marble/Bronze • 0.24% Emissive Accents (`<= 8.0%` Cap)** | — | — | **`788,698.33`** | **`100.00%`** |
