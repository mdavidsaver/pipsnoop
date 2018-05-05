Use travis-ci and appveyor to extract info about various python targets

https://travis-ci.org/mdavidsaver/pipsnoop

https://ci.appveyor.com/project/mdavidsaver/pipsnoop

Useful values to distinguish hosts.
Values for checked on python 2.7, 3.3, 3.4, 3.5, 3.6.

<table>
 <tr><th>Name</th>
     <th>Linux/amd64</th>
     <th>Linux/i686</th>
     <td>OS X/amd64</td>
     <td>Windows/amd64</td>
     <td>Windows/i686</td>
 </tr>
 <tr><td>platform.system()</td>
     <td>"Linux"</td>
     <td>"Linux"</td>
     <td>"Darwin"</td>
     <td>"Windows"</td>
     <td>"Windows"</td>
 </tr>
 <tr><td>platform.architecture()[0]</td>
     <td>"64bit"</td>
     <td>"32bit"</td>
     <td>"64bit"</td>
     <td>"64bit"</td>
     <td>"32bit"</td>
 </tr>
 <tr><td>platform.machine()</td>
     <td>"x86_64"</td>
     <td>"i686"</td>
     <td>"x86_64"</td>
     <td colspan="2">Not correct!</td>
 </tr>
 <tr><td></td>
     <td></td>
     <td></td>
     <td></td>
     <td></td>
 </tr>
</table>
