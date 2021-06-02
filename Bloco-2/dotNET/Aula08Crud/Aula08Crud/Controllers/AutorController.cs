﻿using Aula08Crud.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Aula08Crud.Controllers {
    public class AutorController : Controller {
        private static List<AutorModel> Autores { get; } = new List<AutorModel> {
            new AutorModel {
                Id = 1,
                Nome="Tao",
                UltimoNome = "Hansen",
                Nacionalidade = "Brasileiro",
                Nascimento = new DateTime(1996, 01, 31),
                QuantidadeLivrosPublicados = 1 
            },
            new AutorModel {
                Id = 2,
                Nome="Felipe",
                UltimoNome = "Andrade",
                Nacionalidade = "Brasileiro",
                Nascimento = new DateTime(1988, 04, 12),
                QuantidadeLivrosPublicados = 10
            },
        };

        // GET: AutorController
        public ActionResult Index() {







            return View(Autores);
        }

        // GET: AutorController/Details/5
        public ActionResult Details(int id) {
            return View();
        }

        // GET: AutorController/Create
        public ActionResult Create() {
            return View();
        }

        // POST: AutorController/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Create(AutorModel autorModel) {
            try {
                Autores.Add(autorModel);
                return RedirectToAction(nameof(Index));
            }
            catch {
                return View();
            }
        }

        // GET: AutorController/Edit/5
        public ActionResult Edit(int id) {
            return View();
        }

        // POST: AutorController/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Edit(int id, IFormCollection collection) {
            try {
                return RedirectToAction(nameof(Index));
            }
            catch {
                return View();
            }
        }

        // GET: AutorController/Delete/5
        public ActionResult Delete(int id) {
            return View();
        }

        // POST: AutorController/Delete/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Delete(int id, IFormCollection collection) {
            try {
                return RedirectToAction(nameof(Index));
            }
            catch {
                return View();
            }
        }
    }
}