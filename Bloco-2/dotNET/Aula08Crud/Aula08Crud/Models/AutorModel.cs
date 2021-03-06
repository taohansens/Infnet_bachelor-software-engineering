﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Aula08Crud.Models {
    public class AutorModel {
        public int Id { get; set; }
        public string Nome { get; set; }
        public string UltimoNome { get; set; }
        public string Nacionalidade { get; set; }
        public int QuantidadeLivrosPublicados { get; set; }
        public DateTime Nascimento { get; set; }

        public AutorModel() {

        }

        public AutorModel(int id, string nome, string ultimoNome, 
            string nacionalidade, int quantidadeLivrosPublicados, 
            DateTime nascimento) {

            Id = id;
            Nome = nome;
            UltimoNome = ultimoNome;
            Nacionalidade = nacionalidade;
            QuantidadeLivrosPublicados = quantidadeLivrosPublicados;
            Nascimento = nascimento;
        }
    }
}
