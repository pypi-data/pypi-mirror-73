# coding: utf-8
# author: gabriel couture
from typing import Dict

from pyorthanc import Orthanc


class RemoteModality:
    """Wrapper around Orthanc API when dealing with a (remote) modality.
    """

    def __init__(self, orthanc: Orthanc, modality: str) -> None:
        """Constructor

        Parameters
        ----------
        orthanc
            Orthanc object.
        modality
            Remote modality.
        """
        self.orthanc = orthanc
        self.modality = modality

    def echo(self) -> bool:
        """C-Echo to remote modality

        Returns
        -------
        bool
            True if C-Echo succeeded.
        """
        return self.orthanc.echo_to_modality(self.modality)

    def query(self, data: Dict) -> Dict:
        """C-Find (Querying with data)

        Parameters
        ----------
        data
            Dictionary to send in the body of request.

        Returns
        -------
        Dict
            Dictionary with keys {'ID': '...', 'path': '...'}

        Examples
        -------
        >>> data = {'Level': 'Study',
        ...         'Query': {
        ...             'PatientID':'03HD*',
        ...             'StudyDescription':'*Chest*',
        ...             'PatientName':''
        ...         }
        ... }

        >>> remote_modality = RemoteModality(
        ...     orthanc=Orthanc('http://localhost:8042'),
        ...     modality='sample'
        ... )

        >>> remote_modality.query(data)
        """
        return self.orthanc.query_on_modality(self.modality, data=data)

    def move(self, query_identifier: str, cmove_data: Dict) -> Dict:
        """C-Move query results to another modality

        C-Move SCU: Send all the results to another modality whose AET is in the body

        Parameters
        ----------
        query_identifier
            Query identifier.
        cmove_data
            Ex. {'TargetAet': 'target_modality_name', "Synchronous": False}

        Returns
        -------
        Dict
            Orthanc Response (probably a Dictionary)

        Examples
        --------
        >>> remote_modality = RemoteModality(Orthanc('http://localhost:8042'), 'modality')
        >>> query_id = remote_modality.query(
        ...     data={'Level': 'Series',
        ...           'Query': {'PatientID': '',
        ...                     'Modality':'SR'}})

        >>> remote_modality.move(
        ...     query_identifier=query_id['ID'],
        ...     cmove_data={'TargetAet': 'TARGETAET'}
        ... )

        """
        return self.orthanc.move_query_results_to_given_modality(
            query_identifier,
            cmove_data
        )
