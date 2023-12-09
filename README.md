<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/AndManGames/GameArt">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">GameArt</h3>

  <p align="center">
    Create printable art with the movement of your mouse.
    <br />
    <a href="https://github.com/AndManGames/GameArt"><strong>Explore the source code »</strong></a>
    <br />
    <br />
    <a href="https://github.com/AndManGames/GameArt">View Readme</a>
    ·
    <a href="https://github.com/AndManGames/GameArt/issues">Report Bug</a>
    ·
    <a href="https://github.com/AndManGames/GameArt/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#enhancement">Enhancement</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


<!-- GETTING STARTED -->
## Getting Started

GameArt is still work in progress. Currently it is possible to create a png-file with matplotlib from the recorded mouse movement using pynput. The "Art" aspect is currently missing, but I will work on that.

There are 3 package versions available:
* gameart: This version contains only the possibility to draw a png based on csv input. Also there is no CLI.
* gameart[full]: This version contains additionally the possibility to record your mouse movement and save it as a csv. Also it has a CLI.
* gameart[dev]: Same as [full] but with additional dev packages to be able to contribute to this project.


### Prerequisites

* Supported python versions: Python 3.10, 3.11, 3.12
* Upgrade pip
  ```sh
  pip install --upgrade pip
  ```
* It is recommended to use the package inside a virtual environment.
    * Create virtual environment
    ```sh
    python -m venv env
    ```
    * Activate virtual environment - Linux
    ```sh
    source env/bin/activate
    ```
    * Activate virtual environment - Windows
    ```sh
    env/Scripts/activate
    ```

### Installation

1. From GitHub:
    1. Clone the repo
    ```sh
    git clone https://github.com/AndManGames/GameArt.git
    ```
    2. Install gameart packages from git root path
    ```sh
    pip install .[full]
    ```
2. From Pypi:
  ```sh
  pip install gameart[full]
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

* Start recording your mouse movement:
   ```sh
   gameart record
   ```
* **Stop the recording** by pressing the `Right Mouse Button`

* Generate image from your mouse recording:
   ```sh
   gameart draw --csv_file_path path/to/csv/file
   ```
    * If no output folder is specified the image will be saved to the current_dir/gameart_images.
    * Optionally you can specify an output folder (absolute path) by using the argument `--output_folder`.
    ```sh
    gameart draw --csv_file_path path/to/csv/file --output_folder path/to/output/folder
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Enhancement requests and Issues -->
## Enhancement

See the [open issues](https://github.com/AndManGames/GameArt/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue.
Don't forget to give the project a star! Thanks again!

For contributing please use the dev setup of this package:
  ```sh
  pip install .[dev]
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Andreas Schneider - programmerhumor22@gmail.com

Project Link: [https://github.com/AndManGames/GameArt](https://github.com/AndManGames/GameArt)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/AndManGames/GameArt.svg?style=for-the-badge
[contributors-url]: https://github.com/AndManGames/GameArt/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/AndManGames/GameArt.svg?style=for-the-badge
[forks-url]: https://github.com/AndManGames/GameArt/network/members
[stars-shield]: https://img.shields.io/github/stars/AndManGames/GameArt.svg?style=for-the-badge
[stars-url]: https://github.com/AndManGames/GameArt/stargazers
[issues-shield]: https://img.shields.io/github/issues/AndManGames/GameArt.svg?style=for-the-badge
[issues-url]: https://github.com/AndManGames/GameArt/issues
[license-shield]: https://img.shields.io/github/license/AndManGames/GameArt.svg?style=for-the-badge
[license-url]: https://github.com/AndManGames/GameArt/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png
